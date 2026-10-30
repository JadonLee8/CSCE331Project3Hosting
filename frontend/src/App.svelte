<script lang="ts">
  import Router from 'svelte-spa-router'
  import Landing from './pages/Landing.svelte'
  import About from './pages/About.svelte'
  import Sean from './pages/Sean.svelte'
  import Order from './pages/Order.svelte'
  import PlaceOrder from './pages/PlaceOrder.svelte'

  const routes = {
    '/': Landing,
    '/about': About,
    '/sean': Sean,
    '/order':Order,
    '/order': PlaceOrder,
  }

  ;(window as any).googleTranslateElementInit = () => {
    new (window as any).google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
  }

</script>

<svelte:head>
  <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</svelte:head>
<nav class="flex items-center gap-6 border-b border-line py-4 font-medium">
  <a href="#/" class="mr-auto text-xl font-bold text-primary-dark">Dunsin's Donuts</a>
  <a href="#/about" class="text-muted hover:text-primary">About</a>
  <a href="#/sean" class="text-muted hover:text-primary">Sean</a>
  <a href="#/order" class="rounded bg-primary px-4 py-2 text-white hover:bg-primary-dark">Order Now</a>
</nav>

<Router {routes} />

<footer class="mt-auto flex flex-wrap items-center justify-between gap-3 border-t border-line py-4 text-sm text-muted">
  <p>&copy; {new Date().getFullYear()} Dunsin's Donuts</p>
  <div id="google_translate_element"></div>
</footer>
