<?php

namespace Controller;

use Attributes\Route;
use Exception\ValidationException;
use Http\Request;
use Http\Response;
use Http\View;
use Middleware\Guest;
use Request\LoginRequest;
use Service\AuthenticationService;

readonly class LoginController
{
    #[Route(path: '/login', middlewares: [Guest::class])]
    public function get(): Response
    {
        return View::render('login/index');
    }

    #[Route(path: '/login', method: Request::POST, middlewares: [Guest::class])]
    public function post(AuthenticationService $authenticationService, LoginRequest $loginRequest): Response
    {
        try {
            $validated = $loginRequest->validate();
        } catch (ValidationException $exception) {
            return View::render('login/index', ['errors' => $exception->errors]);
        }

        if (!$authenticationService->login($validated['username'], $validated['password'])) {
            return View::render('login/index', ['errors' => ['password' => 'Invalid credentials']]);
        }

        return Response::redirect('/');
    }
}
