<script lang="ts">
  import Router from 'svelte-spa-router'
  import Landing from './pages/Landing.svelte'
  import About from './pages/About.svelte'
  import Sean from './pages/Sean.svelte'
  import PlaceOrder from './pages/PlaceOrder.svelte'

  const routes = {
    '/': Landing,
    '/about': About,
    '/sean': Sean,
    '/order': PlaceOrder,
  }

  ;(window as any).googleTranslateElementInit = () => {
    new (window as any).google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
  }

</script>

<svelte:head>
  <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</svelte:head>

<nav>
  <a href="#/">Landing</a>
  <a href="#/about">About</a>
  <a href = "#/sean"> Sean </a>
  <a href="#/order">Place Order</a>
</nav>

<Router {routes} />

<footer>
  <p>&copy; {new Date().getFullYear()} Dunsin's Donuts</p>
  <div id="google_translate_element"></div>
</footer>
