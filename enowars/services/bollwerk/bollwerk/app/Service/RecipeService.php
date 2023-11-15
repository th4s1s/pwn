<?php

namespace Service;

use Exception\ValidationException;
use Http\Request;
use Model\Recipe;
use Model\User;

readonly class RecipeService
{
    public function __construct(
        private Request $request,
    ) {
    }

    public function createRecipe(array $data): Recipe
    {
        $directory = resolvePath('files/' . md5($this->request->session->getUser()->username), checkFileExistence: false);

        if (!is_dir($directory)) {
            mkdir(directory: $directory, recursive: true);
        }

        $recipe = Recipe::create([
            'userId' => $this->request->getCurrentUserId(),
            'title' => $data['title'],
            'description' => $data['description'],
        ]);

        $filePath = $directory . DIRECTORY_SEPARATOR . $recipe->title . '.md';

        if (is_file($filePath)) {
            throw new ValidationException(['title' => 'You already created a recipe with that title.']);
        }

        file_put_contents($filePath, <<<FILE
        # $recipe->title
        
        $recipe->description
        FILE);

        return $recipe::update($recipe->id, ['filename' => $filePath]);
    }
}
