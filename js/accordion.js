// Nancy Universe — FAQ Accordion
(function() {
  document.querySelectorAll('.accordion-trigger').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const item = trigger.parentElement;
      const isOpen = item.classList.contains('open');

      // Close all items in same section
      const section = item.closest('.accordion-section') || item.closest('.accordion');
      section.querySelectorAll('.accordion-item.open').forEach(openItem => {
        openItem.classList.remove('open');
      });

      // Open clicked item (if it wasn't already open)
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });
})();
