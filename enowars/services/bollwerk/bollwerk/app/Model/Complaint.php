<?php

namespace Model;

class Complaint extends AbstractModel
{
    public int $id;
    public int $userId;
    public string $description;
    public string $token;
    public int $submittedAt;

    public static function getAllByUser(User|int $id): array
    {
        $id = $id instanceof User ? $id->id : $id;

        $result = static::getDatabase()->fetchAll(
            'SELECT * FROM ' . static::getTableName() . ' WHERE user_id = :userId',
            ['userId' => $id]
        );

        return static::hydrateMany($result);
    }

    public function getUser(): User
    {
        return User::find($this->userId);
    }
}
