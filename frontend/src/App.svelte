<script lang="ts">
  import Router from 'svelte-spa-router'
  import Landing from './pages/Landing.svelte'
  import About from './pages/About.svelte'

  const routes = {
    '/': Landing,
    '/about': About,
  }
</script>

<nav>
  <a href="#/">Landing</a>
  <a href="#/about">About</a>
</nav>

<Router {routes} />