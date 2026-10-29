<script lang="ts">
  import './Landing.css'

  let dbStatus: string = $state('')
  let menuItems: { menu_item_name: string; price: number }[] = $state([])

  async function pingDb() {
    dbStatus = 'Checking...'
    try {
      const res = await fetch('/api/db-ping')
      const body = await res.json()
      dbStatus = body.status
    } catch (err) {
      dbStatus = `Backend unreachable: ${err}`
    }
  }

  async function fetchMenuItems() {
    try {
      const menuItemsResponse = await fetch('/api/menu-items')
      menuItems = await menuItemsResponse.json()
    } catch (err) {
      console.error('Error fetching menu items:', err)
    }
  }
</script>

<style>
  /* This only targets <button> elements inside THIS component */
  button {
    background: royalblue;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
  }

  :root{
    background: grey;
  }
</style>
    
<div class="landing">
<h1>Landing Page</h1>
<p>Welcome to Dunsin's Donuts</p>

<p>Replace with the image for dunsin donuts</p>



<button>Order Now</button>


<button type="button" onclick={fetchMenuItems}>Fetch Menu Items</button>
<p>Menu items:</p>

{#each menuItems as item}
  <span>{item.menu_item_name}: ${item.price}</span>
{/each}

<button type="button" onclick={pingDb}>Test DB connection</button>
<p>{dbStatus}</p>
</div>
