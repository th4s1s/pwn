<?php

namespace Controller;

use Attributes\Route;
use Exception\NotFoundException;
use Exception\ValidationException;
use Http\Request;
use Http\Response;
use Http\View;
use Middleware\Authenticated;
use Model\Recipe;
use Request\CreateRecipeRequest;
use Request\GetRecipeRequest;
use Service\RecipeService;

readonly class RecipeController
{
    #[Route(path: '/recipes', method: Request::POST, middlewares: [Authenticated::class])]
    public function store(CreateRecipeRequest $createRecipeRequest, RecipeService $recipeService): Response
    {
        try {
            $validated = $createRecipeRequest->validate();
        } catch (ValidationException $exception) {
            return View::render('recipes/create', ['errors' => $exception->errors]);
        }

        $recipe = $recipeService->createRecipe($validated);

        return Response::redirect("/recipes/$recipe->id");
    }

    #[Route(path: '/recipes', middlewares: [Authenticated::class])]
    public function get(Request $request, GetRecipeRequest $recipeRequest): Response
    {
        try {
            $validated = $recipeRequest->validate();
        } catch (ValidationException $exception) {
            return View::render('recipes/index', ['recipes' => [], 'errors' => $exception->errors]);
        }

        $recipes = Recipe::searchRecipesByTitle(
            $request->getCurrentUserId(),
            $validated['title'] ?? '',
        );

        return View::render('recipes/index', ['recipes' => $recipes, 'title' => $validated['title'] ?? '']);
    }

    #[Route(path: '/recipes/{recipe}', middlewares: [Authenticated::class])]
    public function show(Request $request, Recipe $recipe): Response
    {
        if ($recipe->userId !== $request->getCurrentUserId()) {
            throw new NotFoundException();
        }

        return View::render('recipes/show', ['recipe' => $recipe]);
    }

    #[Route(path: '/recipes/{recipe}/download', middlewares: [Authenticated::class])]
    public function download(Request $request, Recipe $recipe): Response
    {
        if ($recipe->userId !== $request->getCurrentUserId() || $recipe->filename === null) {
            throw new NotFoundException();
        }

        return Response::file($recipe->filename, $recipe->title . '.md');
    }

    #[Route(path: '/recipes/create', middlewares: [Authenticated::class])]
    public function create(): Response
    {
        return View::render('recipes/create');
    }
}
