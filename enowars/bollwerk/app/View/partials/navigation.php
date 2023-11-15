<nav>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/recipes">My Recipes</a></li>
        <li><a href="/recipes/create">Create Recipe</a></li>
        <li><?= $user ? '<a href="/logout">Logout</a>' : '<a href="/login">Login</a>' ?></li>
    </ul>
</nav>
