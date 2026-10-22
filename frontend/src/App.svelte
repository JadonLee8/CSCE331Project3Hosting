<script>
  import { onMount } from 'svelte'
  import svelteLogo from './assets/svelte.svg'
  import viteLogo from './assets/vite.svg'
  import heroImg from './assets/hero.png'
  import Counter from './lib/Counter.svelte'

  const ENDPOINT = `${import.meta.env.VITE_BACKEND_URL ?? 'http://localhost:8080'}/health`;
  let healthResponse = $state('loading...');

  onMount(async () => {
    try {
      healthResponse = await fetch(ENDPOINT).then((res) => res.text());
    } catch (err) {
      healthResponse = `error: ${err}`;
    }
  });
</script>

<section id="center">
  <div class="hero">
    <img src={heroImg} class="base" width="170" height="179" alt="" />
    <img src={svelteLogo} class="framework" alt="Svelte logo" />
    <img src={viteLogo} class="vite" alt="Vite logo" />
  </div>
  <div>
    <h1>Squad 44</h1>
  </div>
  <Counter />
</section>

<div class="ticks"></div>

<section id="next-steps">
  <div id="docs">
    {healthResponse}
  </div>
</section>

<div class="ticks"></div>
<section id="spacer"></section>
