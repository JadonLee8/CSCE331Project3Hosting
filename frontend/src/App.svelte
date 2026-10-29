<script lang="ts">
  import Router from 'svelte-spa-router'
  import Landing from './pages/Landing.svelte'
  import About from './pages/About.svelte'
  import Sean from './pages/Sean.svelte'
  import Order from './pages/Order.svelte'

  const routes = {
    '/': Landing,
    '/about': About,
    '/sean': Sean,
    '/order':Order,
  }
</script>
<style>
  nav {
    background:pink;
    padding-top: 5px;
    padding-bottom: 5px;
    display:flex;
    justify-content: space-between;
    padding: 1rem; 
    align-items:center;
  }
  .NavigationText{
    color:aliceblue;
    text-decoration: none;
    font-size: 20px
  }
  .order{
    background-color: grey;
    color:white;
    text-decoration: none;
    font-size: 20px;
    gap: 1.5rem
  }
  
</style>
<nav>
  <a href="#/" class = "NavigationText">Dunsin Donuts</a>
  <a href="#/about" class = "NavigationText">About</a>
  <a href = "#/sean" class = "NavigationText"> Sean </a>
  <a href = '#/order' class = "Order">Order Now</a>
</nav>

<Router {routes} />
