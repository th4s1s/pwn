<?php

namespace Controller;

use Attributes\Route;
use Http\Response;
use Middleware\Authenticated;
use Service\AuthenticationService;

readonly class LogoutController
{
    #[Route(path: '/logout', middlewares: [Authenticated::class])]
    public function get(AuthenticationService $authenticationService): Response
    {
        $authenticationService->logout();

        return Response::redirect('/');
    }
}
