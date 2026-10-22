<!-- src/About.svelte -->
<script>
  // You can pass a callback function to go back home
  let { navigate } = $props();
</script>

<section id="center">
  <h1>About Page</h1>
  <p>Welcome to the second page of your Svelte application!</p>
  <button onclick={() => navigate('home')}>Go Back Home</button>
</section>
