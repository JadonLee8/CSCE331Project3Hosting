<script lang="ts">
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
    
<div class="landing">
<h1>Landing Page</h1>
<p>Welcome to Dunsin's Donuts</p>
<button type="button" onclick={fetchMenuItems}>Fetch Menu Items</button>
<p>Menu items:</p>
{#each menuItems as item}
  <span>{item.menu_item_name}: ${item.price}</span>
{/each}

<button type="button" onclick={pingDb}>Test DB connection</button>
<p>{dbStatus}</p>
</div>

<style>
  /* Lock the home page to a single viewport with no page scroll */
  :global(#app:has(> .landing)) {
    height: 100svh;
    overflow: hidden;
  }

  .landing {
    flex: 1 1 0;
    min-height: 0;
    overflow: hidden;
  }
</style>
