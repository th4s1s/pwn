<?php

namespace Http;

class View
{
    private static Request $request;

    public static function create(Request $request): void
    {
        static::$request = $request;
    }

    public static function render(string $view, array $parameters = []): Response
    {
        ob_start();

        $viewPath = "View/$view.php";

        extract([...static::createGlobals(), ...$parameters]);

        require(resolvePath($viewPath));

        return Response::create((string)ob_get_clean());
    }

    private static function createGlobals(): array
    {
        return [
            'user' => static::$request->session->getUser(), ...static::$request->cookie,
        ];
    }
}
