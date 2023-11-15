<?php

namespace Model;

use Exception\NotFoundException;
use Model\AbstractModel;

class User extends AbstractModel
{
    public int $id;
    public string $username;
    public string $password;

    public static function getByUsername(string $username): User
    {
        $user = static::findByUsername($username);

        if (!$user) {
            throw new NotFoundException("Could not find user with username $username");
        }

        return $user;
    }

    public static function findByUsername(string $username): ?User
    {
        return static::findOneBy(['username' => $username]);
    }

    public static function findByCredentials(string $username, string $password): ?User
    {
        return static::findOneBy(['username' => $username, 'password' => $password]);
    }
}
