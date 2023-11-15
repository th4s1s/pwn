<?php

namespace Core;

use Database\Database;
use Exception\NotAuthenticatedException;
use Exception\NotFoundException;
use Http\Request;
use Http\Response;
use Http\Router;
use Http\View;
use Throwable;

readonly class Kernel
{
    public function __construct(
        private Router $router,
        private Request $request,
    ) {
    }

    public static function make(): Kernel
    {
        $router = new Router();

        $router->registerFromAttributes(array_map(
            static fn($controller) => 'Controller\\' . str_replace('/', '\\', basename($controller, '.php'))
            , glob('../Controller/*.php')
        ));

        $request = App::resolve(Request::class);

        View::create($request);

        return new self(
            router: $router,
            request: $request,
        );
    }

    public function handle(): void
    {
        try {
            echo $this->router->resolve($this->request)::getContent();
        } catch (NotFoundException) {
            echo View::render('errors/404')::getContent();
        } catch (NotAuthenticatedException) {
            echo Response::redirect('/login')::getContent();
        } catch (Throwable) {
            echo View::render('errors/500')::getContent();
        }

        /** @var Database $database */
        $database = App::resolve(Database::class);
        $database->close();
    }
}
