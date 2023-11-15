<?php

namespace Model;

class Recipe extends AbstractModel
{
    public int $id;
    public int $userId;
    public string $title;
    public string $description;
    public ?string $filename;

    public static function getAllByUser(User|int $id): array
    {
        $id = $id instanceof User ? $id->id : $id;

        $result = static::getDatabase()->fetchAll(
            'SELECT * FROM ' . static::getTableName() . ' WHERE user_id = :userId',
            ['userId' => $id]
        );

        return static::hydrateMany($result);
    }

    public static function searchRecipesByTitle(int $userId, string $title): array
    {
        $result = static::getDatabase()->fetchAll(
            'SELECT * FROM ' . static::getTableName() . " WHERE user_id = :userId AND title like :title COLLATE NOCASE",
            [
                'userId' => $userId,
                'title' => "%$title%"
            ]
        );

        return static::hydrateMany($result);
    }
}
