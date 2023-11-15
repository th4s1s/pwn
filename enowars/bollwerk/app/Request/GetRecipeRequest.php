<?php

namespace Request;

class GetRecipeRequest extends AbstractRequest
{
    public array $rules = [
        'title' => 'string->optional|max:255',
    ];

    public array $messages = [
        'title' => 'Please provide at most 255 characters',
    ];
}
