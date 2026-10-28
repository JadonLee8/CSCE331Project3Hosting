<script lang="ts">
  let dbStatus: string = $state('')
  let menuItems: { name: string; price: number }[] = $state([])

  async function pingDb() {
    dbStatus = 'Checking...'
    try {
      const res = await fetch('/api/db-ping')
      const body = await res.json()
      const menuItemsResponse = await fetch('/api/menu-items')
      menuItems = await menuItemsResponse.json()
      dbStatus = body.status
    } catch (err) {
      dbStatus = `Backend unreachable: ${err}`
    }
  }
</script>
    
<h1>Landing Page</h1>
<p>Welcome to Dunsin's Donuts</p>
{#each menuItems as item}
  <span>{item.name}: ${item.price}</span>
{/each}

<button type="button" onclick={pingDb}>Test DB connection</button>
<p>{dbStatus}</p>
