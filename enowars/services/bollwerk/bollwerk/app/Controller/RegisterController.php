<?php

namespace Controller;

use Attributes\Route;
use Exception\ValidationException;
use Http\Request;
use Http\Response;
use Http\View;
use Middleware\Guest;
use Model\User;
use Request\RegisterRequest;
use Service\AuthenticationService;

readonly class RegisterController
{
    #[Route(path: '/register', middlewares: [Guest::class])]
    public function get(): Response
    {
        return View::render('register/index');
    }

    #[Route(path: '/register', method: Request::POST, middlewares: [Guest::class])]
    public function post(AuthenticationService $authenticationService, RegisterRequest $registerRequest): Response
    {
        try {
            $validated = $registerRequest->validate();
        } catch (ValidationException $exception) {
            return View::render('register/index', ['errors' => $exception->errors]);
        }

        $user = User::findByUsername($validated['username']);

        if ($user) {
            return View::render('register/index', ['errors' => ['username' => 'User ' . $validated['username'] . ' already exists.']]);
        }

        $authenticationService->register($validated['username'], $validated['password']);

        return Response::redirect('/');
    }
}
