<script lang="ts">
  import Router from 'svelte-spa-router'
  import Landing from './pages/Landing.svelte'
  import About from './pages/About.svelte'
  import Sean from './pages/Sean.svelte'

  const routes = {
    '/': Landing,
    '/about': About,
    '/sean': Sean,
  }
</script>

<nav>
  <a href="#/">Landing</a>
  <a href="#/about">About</a>
  <a href = "#/sean"> Sean </a>
</nav>

<Router {routes} />
