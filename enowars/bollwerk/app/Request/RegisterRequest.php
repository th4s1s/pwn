<?php

namespace Request;

class RegisterRequest extends AbstractRequest
{
    public array $rules = [
        'username' => 'string->required|min:4|max:12',
        'password' => 'string->required|min:4|max:255',
    ];

    public array $messages = [
        'username' => 'Please provide a username between 4 and 12 characters',
        'password' => 'Please provide a password between 4 and 255 characters',
    ];
}
