(function(){
  const key='capstone-theme';
  const root=document.documentElement;
  const stored=localStorage.getItem(key);
  if(stored==='dark') root.dataset.theme='dark';
  if(stored==='light') root.dataset.theme='light';

  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('[data-action="toggle-theme"]');
    if(!btn) return;
    const current = root.dataset.theme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark':'light');
    const next = current==='dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    localStorage.setItem(key, next);
  });
})();
