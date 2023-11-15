<?php

namespace Core;

use ReflectionClass;
use ReflectionNamedType;
use ReflectionParameter;
use ReflectionUnionType;
use RuntimeException;

class ServiceContainer
{
    private array $bindings = [];

    public function bind($key, $resolver): void
    {
        $this->bindings[$key] = $resolver;
    }

    public function get($key)
    {
        if (array_key_exists($key, $this->bindings)) {
            return call_user_func($this->bindings[$key]);
        }

        return $this->resolve($key);
    }

    private function resolve($key)
    {
        $reflectionClass = new ReflectionClass($key);

        if (!$reflectionClass->isInstantiable()) {
            throw new RuntimeException("Could not instantiate binding $key");
        }

        $constructor = $reflectionClass->getConstructor();

        if (!$constructor) {
            return new $key;
        }

        $parameters = $constructor->getParameters();

        if (!$parameters) {
            return new $key;
        }

        $dependencies = array_map(function (ReflectionParameter $parameter) use ($key) {
            $type = $parameter->getType();

            if (!$type) {
                throw new RuntimeException("Could not resolve class $key");
            }

            if ($type instanceof ReflectionUnionType) {
                throw new RuntimeException("Could not resolve union type $type for $key");
            }

            if ($type instanceof ReflectionNamedType && !$type->isBuiltin()) {
                return $this->get($type->getName());
            }

            throw new RuntimeException("Could not resolve class $key");
        }, $parameters);


        return $reflectionClass->newInstanceArgs($dependencies);
    }
}