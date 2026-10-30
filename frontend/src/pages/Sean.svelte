

<h1 class="mt-8 mb-4 text-4xl font-semibold tracking-tight text-primary-dark"> hi im sean </h1>

<script>
  // This runs when the component initializes
  console.log("Component has loaded!");
  function showAlert() {
    alert("Hello from Svelte!");
  }
  function callBackend(){

  }
</script>

<button class="btn" onclick={showAlert}>Show Native Alert</button>
<button class="btn" onclick={callBackend}>Call Backend</button>