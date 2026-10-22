

<h1> hi im sean </h1>

<script>
  // This runs when the component initializes
  console.log("Component has loaded!");
  function showAlert() {
    alert("Hello from Svelte!");
  }
  function callBackend(){

  }
</script>

<button onclick={showAlert}>Show Native Alert</button>
<button onclick={callBackend}>Call Backend</button>