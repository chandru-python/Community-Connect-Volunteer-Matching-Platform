/* =========================================================
   Community Connect — script.js
   Interactive behaviors & UI enhancements
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. Animated stat counters on home page ── */
  const counterEls = document.querySelectorAll('.stat-number[data-target]');
  if (counterEls.length) {
    const animateCounter = (el) => {
      const target = parseInt(el.dataset.target, 10);
      if (isNaN(target) || target === 0) { el.textContent = '0'; return; }
      const duration = 1400;
      const step = Math.ceil(target / (duration / 16));
      let current = 0;
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current.toLocaleString();
        if (current >= target) clearInterval(timer);
      }, 16);
    };

    // Use IntersectionObserver for scroll-triggered animation
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });

    counterEls.forEach(el => observer.observe(el));
  }

  /* ── 2. Password visibility toggle ── */
  document.querySelectorAll('.toggle-pw').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.closest('.input-group').querySelector('input[type="password"], input[type="text"]');
      if (!input) return;
      const isHidden = input.type === 'password';
      input.type = isHidden ? 'text' : 'password';
      btn.querySelector('i').className = isHidden ? 'bi bi-eye-slash' : 'bi bi-eye';
    });
  });

  /* ── 3. Password strength indicator ── */
  const pwInput = document.getElementById('password');
  const pwStrength = document.getElementById('pwStrength');
  if (pwInput && pwStrength) {
    pwInput.addEventListener('input', () => {
      const val = pwInput.value;
      let score = 0;
      if (val.length >= 6)  score++;
      if (val.length >= 10) score++;
      if (/[A-Z]/.test(val)) score++;
      if (/[0-9]/.test(val)) score++;
      if (/[^A-Za-z0-9]/.test(val)) score++;

      const levels = [
        { w: '0%',   color: '#ccc' },
        { w: '25%',  color: '#ef4444' },
        { w: '50%',  color: '#f59e0b' },
        { w: '75%',  color: '#3b82f6' },
        { w: '100%', color: '#22c55e' },
      ];
      const level = levels[Math.min(score, 4)];
      pwStrength.style.setProperty('--pw-width', level.w);
      pwStrength.style.setProperty('--pw-color', level.color);
    });
  }

  /* ── 4. Demo login quick-fill buttons ── */
  document.querySelectorAll('.demo-fill').forEach(btn => {
    btn.addEventListener('click', () => {
      const emailEl = document.getElementById('email');
      const pwEl    = document.getElementById('password');
      if (emailEl) emailEl.value = btn.dataset.email;
      if (pwEl)    pwEl.value    = btn.dataset.pw;
    });
  });

  /* ── 5. Apply button micro-interaction ── */
  document.querySelectorAll('.apply-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const original = this.innerHTML;
      this.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Applying…';
      this.disabled = true;
      // Form submits naturally; this just gives visual feedback
      setTimeout(() => {
        this.innerHTML = original;
        this.disabled = false;
      }, 3000);
    });
  });

  /* ── 6. Auto-dismiss flash alerts after 5 s ── */
  document.querySelectorAll('.alert.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  /* ── 7. Fade-in cards on scroll ── */
  const fadeEls = document.querySelectorAll(
    '.project-card, .how-card, .stat-card, .cc-card, .quick-action-card'
  );
  if (fadeEls.length) {
    const fadeObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, i * 60);
          fadeObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    fadeEls.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity .5s ease, transform .5s ease';
      fadeObserver.observe(el);
    });
  }

  /* ── 8. Date validation: end ≥ start ── */
  const startDate = document.getElementById('start_date');
  const endDate   = document.getElementById('end_date');
  if (startDate && endDate) {
    startDate.addEventListener('change', () => {
      endDate.min = startDate.value;
      if (endDate.value && endDate.value < startDate.value) {
        endDate.value = startDate.value;
      }
    });
  }

  /* ── 9. Live search debounce (projects page) ── */
  const searchInput = document.querySelector('input[name="search"]');
  const searchForm  = document.getElementById('searchForm');
  if (searchInput && searchForm) {
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => searchForm.submit(), 600);
    });
  }

  /* ── 10. Navbar active link highlighting ── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.cc-navbar .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      link.classList.add('active');
      link.style.color = 'var(--cc-green)';
      link.style.background = 'var(--cc-green-pale)';
    }
  });

});
