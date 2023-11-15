<?php

namespace Http;

use Exception\NotFoundException;

class Response
{
    private static string $content = '';

    public static function redirect(string $uri): static
    {
        header("Location: $uri");
        return new static();
    }

    public static function json(array $data): static
    {
        self::$content = json_encode($data);
        return new static();
    }

    public static function file(string $path, ?string $filename = null): static
    {
        if (!is_file($path)) {
            throw new NotFoundException();
        }

        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . $filename ?? 'file' . '"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($path));

        self::$content = readfile($path);
        return new static();
    }

    public static function create(string $content): static
    {
        self::$content = $content;
        return new static();
    }

    public static function getContent(): string
    {
        return self::$content;
    }
}
