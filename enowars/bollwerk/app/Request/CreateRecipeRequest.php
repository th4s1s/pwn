<?php

namespace Request;

use Exception\ValidationException;
use Model\Recipe;
use Validator\Validator;

class CreateRecipeRequest extends AbstractRequest
{
    public array $rules = [
        'title' => 'string->min:1|max:255',
        'description' => 'string->min:1|max:255',
    ];

    public array $messages = [
        'title' => 'Please provide a title with at most 255 characters',
        'description' => 'Please provide a description at most 255 characters',
    ];

    public function validate(): array
    {
        $validated = Validator::validate($this->data, $this->rules, $this->messages);

        $replacedTitle = preg_replace('/[^a-zA-Z0-9 ]/', '', $validated['title']);

        if ($replacedTitle !== $validated['title']) {
            throw new ValidationException(['title' => 'Please only use alphanumeric characters']);
        }

        if (Recipe::findOneBy([
                'userId' => $this->request->getCurrentUserId(),
                'title' => $validated['title'],
            ]) !== null) {
            throw new ValidationException(['title' => 'You already created a recipe with that title']);
        }

        return $validated;
    }
}
