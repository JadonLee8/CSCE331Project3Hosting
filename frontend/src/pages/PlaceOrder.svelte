<script lang="ts">
  import './PlaceOrder.css'

  type MenuItem = {
    menu_item_id: number
    menu_item_name: string
    price: number
    category?: string
  }

  let menuItems: MenuItem[] = $state([])
  let selectedCategory: string = $state('All')

  let categories = $derived([
    'All',
    ...new Set(menuItems.map((item) => item.category ?? 'Other')),
  ])

  let visibleItems = $derived(
    selectedCategory === 'All'
      ? menuItems
      : menuItems.filter((item) => (item.category ?? 'Other') === selectedCategory)
  )

  async function fetchMenuItems() {
    try {
      const menuItemsResponse = await fetch('/api/menu-items')
      menuItems = await menuItemsResponse.json()
    } catch (err) {
      console.error('Error fetching menu items:', err)
    }
  }

  $effect(() => {
    fetchMenuItems()
  })
</script>

<div class="place-order">
  <aside class="categories">
    {#each categories as category}
      <button
        type="button"
        class:selected={category === selectedCategory}
        onclick={() => (selectedCategory = category)}
      >
        {category}
      </button>
    {/each}
  </aside>

  <main class="menu-grid">
    {#each visibleItems as item (item.menu_item_id)}
      <button type="button" class="menu-item">
        <span>{item.menu_item_name}</span>
        <span>${item.price.toFixed(2)}</span>
      </button>
    {/each}
  </main>
</div>
