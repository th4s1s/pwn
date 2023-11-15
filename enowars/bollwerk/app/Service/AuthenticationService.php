<?php

namespace Service;

use Http\Request;
use Model\User;

readonly class AuthenticationService
{
    public function __construct(
        private Request $request,
    ) {
    }

    public function login(string $username, string $password): bool
    {
        $user = User::findByCredentials($username, md5($password));

        if (!$user) {
            return false;
        }

        $this->request->session->setUser($user);

        session_regenerate_id();

        return true;
    }

    public function logout(): void
    {
        $this->request->session->invalidate();
    }

    public function register(string $username, string $password): void
    {
        $user = User::create(['username' => $username, 'password' => md5($password)]);

        $this->request->session->setUser($user);

        session_regenerate_id();
    }
}
