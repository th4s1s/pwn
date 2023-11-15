<?php

namespace Database;

use SQLite3;

readonly class Database
{
    private SQLite3 $database;

    public function __construct(string $path)
    {
        $this->database = new SQLite3($path, SQLITE3_OPEN_READWRITE);
        $this->database->busyTimeout(15000);
        $this->database->exec("PRAGMA journal_mode = WAL");
        $this->database->exec("PRAGMA synchronous = normal");
        $this->database->exec("PRAGMA temp_storage = memory");
        $this->database->exec("PRAGMA mmap_size = 30000000000");
        $this->database->exec("PRAGMA page_size = 32768");
    }

    public function close(): void
    {
        $this->database->close();
    }

    public function getLastId(): int
    {
        return $this->database->lastInsertRowID();
    }

    public function fetchSingle(string $query, array $parameters = []): ?array
    {
        $query = $this->database->prepare($query);

        foreach ($parameters as $name => $value) {
            $query->bindValue($name, $value);
        }

        $result = $query->execute();

        if (!$result) {
            return null;
        }

        return $result->fetchArray() ?: null;
    }

    public function fetchAll(string $query, array $parameters = []): ?array
    {
        $query = $this->database->prepare($query);

        foreach ($parameters as $name => $value) {
            $query->bindValue($name, $value);
        }

        $result = $query->execute();

        if (!$result) {
            return null;
        }

        $rows = [];
        while ($row = $result->fetchArray()) {
            $rows[] = $row;
        }

        return $rows;
    }

    public function execute(string $query, array $parameters = []): void
    {
        $query = $this->database->prepare($query);

        foreach ($parameters as $name => $value) {
            $query->bindValue($name, $value);
        }

        $query->execute();
    }
}
