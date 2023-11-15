<?php

namespace Http;

use Attributes\Route;
use Closure;
use Core\App;
use Exception\NotFoundException;
use Model\AbstractModel;
use ReflectionClass;
use ReflectionIntersectionType;
use ReflectionMethod;
use ReflectionNamedType;
use ReflectionUnionType;
use Request\AbstractRequest;
use RuntimeException;

class Router
{
    private array $routes = [];

    public function resolve(Request $request): Response
    {
        $uri = explode('?', $request->requestUri)[0];

        $segments = $this->getRouteSegments($uri);

        $route = array_key_exists($uri, $this->routes[$request->requestMethod])
            ? $this->routes[$request->requestMethod][$uri]
            : $this->getRouteWithParameters($request->requestMethod, $segments);

        $middlewares = $route['middlewares'] ?? [];

        foreach ($middlewares as $middleware) {
            $middleware = App::resolve($middleware);
            $middleware->hande($request);
        }

        if ($route['action'] instanceof Closure) {
            return call_user_func_array($route['action'], [$request]);
        }

        [$class, $action] = $route['action'];

        if (class_exists($class)) {
            $class = App::resolve($class);

            if (method_exists($class, $action)) {
                return call_user_func_array([$class, $action],
                    $this->resolveParameters($class, $action, $route['parameters'], $segments, $request));
            }
        }

        throw new NotFoundException("Could not find route $request->requestUri for method $request->requestMethod");
    }

    private function getRouteWithParameters(string $method, array $segments): array
    {
        foreach ($this->routes[$method] as $uri => $route) {
            if (count($route['parameters']) === 0) {
                continue;
            }

            $convertedUri = $this->getRouteFromSegments($segments, $route['parameters']);

            if ($convertedUri !== null && rtrim($convertedUri, '/') === $uri) {
                return $route;
            }
        }

        throw new NotFoundException('Could not resolve route with parameters.');
    }

    private function resolveParameters(
        object $class,
        string $action,
        array $pathParameters,
        array $segments,
        Request $request
    ): array {
        $reflectionMethod = new ReflectionMethod($class, $action);
        $methodParameters = $reflectionMethod->getParameters();

        $parameters = [];
        foreach ($methodParameters as $parameter) {
            $type = $parameter->getType();
            $name = $parameter->getName();
            if (!$type) {
                throw new RuntimeException("Could not bind parameter $name");
            }

            if ($type instanceof ReflectionUnionType) {
                throw new RuntimeException("Could not resolve union type $type for $name");
            }

            if ($type instanceof ReflectionIntersectionType) {
                throw new RuntimeException("Could not resolve intersection type $type for $name");
            }

            $routeParameter = $this->resolvePathParameterValue($pathParameters, $name, $type, $segments);

            if ($routeParameter !== null) {
                $parameters[] = $routeParameter;
                continue;
            }

            if ($type->isBuiltin()) {
                throw new RuntimeException("Could not resolve builtin type $type for $name");
            }

            if (is_subclass_of($type->getName(), AbstractRequest::class)) {
                $class = $type->getName();
                $parameters[] = new $class($request);
                continue;
            }

            $parameters[] = App::resolve($type);
        }

        return $parameters;
    }

    private function resolvePathParameterValue(
        array $pathParameters,
        string $name,
        ReflectionNamedType $type,
        array $segments
    ): mixed {
        foreach ($pathParameters as $index => $pathParameter) {
            if ($pathParameter === $name) {
                if ($type->isBuiltin()) {
                    return $segments[$index];
                }

                if (is_subclass_of($type->getName(), AbstractModel::class)) {
                    return $type->getName()::find((int)$segments[$index]) ?? throw new NotFoundException();
                }
            }
        }

        return null;
    }

    public function registerFromAttributes(array $controllers): void
    {
        foreach ($controllers as $controller) {
            $reflectionClass = new ReflectionClass($controller);

            foreach ($reflectionClass->getMethods() as $method) {
                $attributes = $method->getAttributes(Route::class);

                foreach ($attributes as $attribute) {
                    /** @var Route $route */
                    $route = $attribute->newInstance();
                    $this->add($route->path, [$controller, $method->getName()], $route->method, $route->middlewares);
                }
            }
        }
    }

    public function add(string $uri, array|callable $action, string $method, array $middlewares): void
    {
        $this->routes[$method][$uri]['action'] = $action;
        $this->routes[$method][$uri]['middlewares'] = $middlewares;
        $this->routes[$method][$uri]['parameters'] = $this->getPathParameters($this->getRouteSegments($uri));
    }

    public function get(string $uri, array|callable $action, array $middlewares): void
    {
        $this->add($uri, $action, Request::GET, $middlewares);
    }

    public function post(string $uri, array|callable $action, array $middlewares): void
    {
        $this->add($uri, $action, Request::POST, $middlewares);
    }

    private function getPathParameters(array $segments): array
    {
        if (count($segments) === 0) {
            return [];
        }

        $parameters = [];
        foreach ($segments as $index => $segment) {
            if (preg_match('/(?<={).+?(?=})/', $segment, $match)) {
                $parameters[$index] = $match[0];
            }
        }

        return $parameters;
    }

    private function getRouteFromSegments(array $segments, array $parameters): ?string
    {
        if (count($segments) < count($parameters)) {
            return null;
        }

        foreach ($parameters as $index => $parameter) {
            if (!array_key_exists($index, $segments) || $segments[$index] === '') {
                return null;
            }

            $segments[$index] = '{' . $parameter . '}';
        }

        return implode('/', $segments);
    }

    private function getRouteSegments(string $uri): array
    {
        return $uri === '' ? [] : explode('/', $uri);
    }
}
