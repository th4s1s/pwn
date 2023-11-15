<?php

namespace Http;

use Model\User;

class Session
{
    private ?User $user;

    public static function create(): self
    {
        $session = new self();
        $userId = $_SESSION['userId'] ?? null;

        $session->user = $userId ? User::find($userId) : null;

        return $session;
    }

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(?User $user): void
    {
        $_SESSION['userId'] = $user->id;
        $this->user = $user;
    }

    public function invalidate(): void
    {
        unset($_SESSION['userId']);
        session_regenerate_id();
    }
}
