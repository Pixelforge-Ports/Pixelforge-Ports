const search = document.querySelector('#search');
const genre = document.querySelector('#genre');
const cards = [...document.querySelectorAll('.game-card')];
function filterPorts() {
  const query = search.value.trim().toLowerCase();
  let count = 0;
  for (const card of cards) {
    const match = card.dataset.title.includes(query) && (!genre.value || card.dataset.genres.split(' ').includes(genre.value));
    card.hidden = !match;
    if (match) count++;
  }
  document.querySelector('#result-count').textContent = `Showing ${count} ${count === 1 ? 'port' : 'ports'}`;
  document.querySelector('#empty').hidden = count !== 0;
}
search.addEventListener('input', filterPorts);
genre.addEventListener('change', filterPorts);
document.querySelector('#reset').addEventListener('click', () => {
  search.value = ''; genre.value = ''; filterPorts(); search.focus();
});
if (document.modelContext?.registerTool) {
  const lifecycle = new AbortController();
  try {
    Promise.resolve(document.modelContext.registerTool({
      name: 'filter_port_catalog',
      description: 'Filter the visible PixelForge port catalog by game title and optional genre, and return matching installation-guide links.',
      inputSchema: {type: 'object', properties: {query: {type: 'string'}, genre: {type: 'string'}}, required: ['query'], additionalProperties: false},
      annotations: {readOnlyHint: false, untrustedContentHint: false},
      execute(input) {
        if (!input || typeof input.query !== 'string' || (input.genre !== undefined && typeof input.genre !== 'string')) throw new Error('Expected query and optional genre strings.');
        const selected = input.genre || '';
        if (![...genre.options].some(option => option.value === selected)) throw new Error('Unknown genre.');
        search.value = input.query; genre.value = selected; filterPorts();
        return {ports: cards.filter(card => !card.hidden).map(card => ({title: card.querySelector('h3').textContent, guide: card.querySelector('h3 a').href}))};
      }
    }, {signal: lifecycle.signal})).catch(() => {});
  } catch { /* The standard catalog remains available without this optional API. */ }
  window.addEventListener('pagehide', () => lifecycle.abort(), {once: true});
}
