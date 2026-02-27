// System Control Client — kill-switch + trial management
(function() {
  const SYSTEM_ID = 'sms-system';
  const STATUS_URL = 'https://api.github.com/repos/smscompany26/system-status/contents/status.json';
  const CHECK_INTERVAL = 60000;
  
  async function fetchStatus() {
    // Try GitHub API (no cache)
    try {
      const res = await fetch(STATUS_URL + '?t=' + Date.now(), {
        headers: { 'Accept': 'application/vnd.github.v3+json' }
      });
      if (res.ok) {
        const ghData = await res.json();
        const raw = atob(ghData.content.replace(/\n/g, ''));
        return JSON.parse(decodeURIComponent(escape(raw)));
      }
    } catch(e) {}
    // Fallback: raw URL
    try {
      const res = await fetch('https://raw.githubusercontent.com/smscompany26/system-status/main/status.json?t=' + Date.now());
      if (res.ok) return await res.json();
    } catch(e) {}
    return null;
  }
  
  async function checkStatus() {
    const data = await fetchStatus();
    if (!data) return;
    
    const sys = data.systems && data.systems[SYSTEM_ID];
    if (!sys) return;
    // Contact info encoded (not plaintext in public repo)
    const owner = { label: (data.contact||{}).label || 'تواصل مع المطور' };
    
    // 1. Disabled permanently
    if (sys.status === 'disabled') {
      showBlockScreen(owner, 'permanent');
      return;
    }
    
    // 2. Temp disabled
    if (sys.status === 'temp-disabled' && sys.disableUntil) {
      if (new Date(sys.disableUntil) > new Date()) {
        showBlockScreen(owner, 'temporary', new Date(sys.disableUntil));
        return;
      }
    }
    
    // 3. Trial check
    if (sys.trial && sys.trial.enabled) {
      const endDate = new Date(sys.trial.endDate);
      const now = new Date();
      const diff = endDate - now;
      
      if (diff <= 0) {
        showBlockScreen(owner, 'trial-expired');
        return;
      }
      
      const days = Math.ceil(diff / 86400000);
      if (days <= (sys.trial.warnDays || 3)) {
        showTrialPopup(owner, days, endDate, sys.trial);
      }
    }
    
    // 4. All good — remove block if exists
    removeBlockScreen();
  }
  
  function showBlockScreen(owner, type, until) {
    if (document.getElementById('system-blocked')) {
      if (until) updateBlockCountdown(until);
      return;
    }
    
    let title, msg, countdownHTML = '';
    if (type === 'trial-expired') {
      title = 'انتهت الفترة التجريبية';
      msg = 'انتهت الفترة التجريبية لهذا النظام.<br>للاستمرار في الاستخدام، يرجى التواصل مع المطور لترقية الاشتراك.';
    } else if (type === 'temporary') {
      title = 'النظام معطّل مؤقتاً';
      msg = 'تم تعطيل النظام مؤقتاً.<br>يرجى الانتظار أو التواصل مع المطور.';
      countdownHTML = '<div id="block-cd" style="font-family:monospace;font-size:20px;color:#d29922;margin:16px 0;direction:ltr;letter-spacing:2px;"></div>';
    } else {
      title = 'النظام معطّل';
      msg = 'تم تعطيل هذا النظام.<br>للاستفسار أو إعادة التفعيل، يرجى التواصل مع المطور.';
    }
    
    const overlay = document.createElement('div');
    overlay.id = 'system-blocked';
    overlay.innerHTML = '<style>' +
      '#system-blocked{position:fixed;inset:0;z-index:999999;background:rgba(10,14,20,0.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);display:flex;align-items:center;justify-content:center;font-family:Cairo,Segoe UI,sans-serif;direction:rtl;padding:20px;}' +
      '.blk-box{text-align:center;max-width:420px;width:100%;}' +
      '.blk-icon{font-size:56px;margin-bottom:16px;}' +
      '.blk-title{color:#f85149;font-size:22px;font-weight:700;margin-bottom:10px;line-height:1.4;}' +
      '.blk-msg{color:#a0a0b8;font-size:14px;line-height:1.8;margin-bottom:20px;}' +
      '.blk-contact{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:20px;margin-top:16px;}' +
      '.blk-contact-title{color:#e6edf3;font-size:13px;font-weight:600;margin-bottom:12px;}' +
      '.blk-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;}' +
      '.blk-btn{display:inline-flex;align-items:center;gap:6px;padding:10px 18px;border-radius:10px;text-decoration:none;font-size:13px;font-weight:600;transition:all 0.2s;font-family:inherit;}' +
      '.blk-wa{background:rgba(37,211,102,0.15);color:#25d366;}.blk-wa:hover{background:rgba(37,211,102,0.25);}' +
      '.blk-call{background:rgba(88,166,255,0.15);color:#58a6ff;}.blk-call:hover{background:rgba(88,166,255,0.25);}' +
      '.blk-web{background:rgba(188,140,255,0.15);color:#bc8cff;}.blk-web:hover{background:rgba(188,140,255,0.25);}' +
      '</style>' +
      '<div class="blk-box">' +
        '<div class="blk-icon">' + (type === 'trial-expired' ? '⏰' : '🚫') + '</div>' +
        '<div class="blk-title">' + title + '</div>' +
        '<div class="blk-msg">' + msg + '</div>' +
        countdownHTML +
        '<div class="blk-contact">' +
          '<div class="blk-contact-title">تواصل مع المطور</div>' +
          '<div class="blk-btns">' +
            '<a href="https://wa.me/' + atob('MjAxMjI4MzcwODA5') + '?text=' + encodeURIComponent('مرحبا، أحتاج مساعدة بخصوص النظام') + '" target="_blank" class="blk-btn blk-wa">💬 واتساب</a>' +
            '<a href="tel:' + atob('MDEyMjgzNzA4MDk=') + '" class="blk-btn blk-call">📱 اتصل بنا</a>' +
          '</div>' +
        '</div>' +
      '</div>';
    document.body.appendChild(overlay);
    
    if (type === 'temporary' && until) {
      updateBlockCountdown(until);
      setInterval(function() { updateBlockCountdown(until); }, 1000);
    }
  }
  
  function updateBlockCountdown(until) {
    var el = document.getElementById('block-cd');
    if (!el) return;
    var diff = until - new Date();
    if (diff <= 0) { location.reload(); return; }
    var d = Math.floor(diff/86400000);
    var h = Math.floor((diff%86400000)/3600000);
    var m = Math.floor((diff%3600000)/60000);
    var s = Math.floor((diff%60000)/1000);
    el.textContent = d + 'd ' + String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
  }
  
  function showTrialPopup(owner, days, endDate, trial) {
    if (document.getElementById('trial-overlay')) return;
    var dismissed = localStorage.getItem('trial_dismissed');
    if (dismissed === new Date().toDateString()) return;
    
    var overlay = document.createElement('div');
    overlay.id = 'trial-overlay';
    overlay.innerHTML = '<style>' +
      '#trial-overlay{position:fixed;inset:0;z-index:99998;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;font-family:Cairo,sans-serif;direction:rtl;padding:20px;animation:trFade 0.3s ease;}' +
      '@keyframes trFade{from{opacity:0}to{opacity:1}}' +
      '.tr-box{background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid rgba(108,60,233,0.3);border-radius:20px;padding:28px 24px;max-width:380px;width:100%;text-align:center;animation:trSlide 0.3s ease;}' +
      '@keyframes trSlide{from{transform:translateY(20px);opacity:0}to{transform:translateY(0);opacity:1}}' +
      '.tr-icon{font-size:44px;margin-bottom:12px;}' +
      '.tr-title{color:#fff;font-size:18px;font-weight:700;margin-bottom:8px;}' +
      '.tr-days{font-size:48px;font-weight:800;color:#f85149;line-height:1;margin:12px 0;}' +
      '.tr-sub{color:#a0a0b8;font-size:13px;margin-bottom:6px;}' +
      '.tr-msg{color:#8888a8;font-size:12px;line-height:1.6;margin-bottom:20px;}' +
      '.tr-btns{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;}' +
      '.tr-btn{padding:10px 20px;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;border:none;font-family:inherit;transition:all 0.2s;}' +
      '.tr-primary{background:linear-gradient(135deg,#6c3ce9,#8b5cf6);color:#fff;text-decoration:none;}' +
      '.tr-primary:hover{transform:scale(1.03);}' +
      '.tr-secondary{background:rgba(255,255,255,0.08);color:#a0a0b8;border:1px solid rgba(255,255,255,0.1);}' +
      '</style>' +
      '<div class="tr-box">' +
        '<div class="tr-icon">⏰</div>' +
        '<div class="tr-title">الفترة التجريبية على وشك الانتهاء</div>' +
        '<div class="tr-days">' + days + '</div>' + '<div style="color:#a0a0b8;font-size:14px;margin-bottom:8px;">أيام</div>' +
        '<div style="font-size:13px;color:#d29922;margin-bottom:16px;">ينتهي في: ' + endDate.toLocaleDateString('ar-EG', {year:'numeric',month:'long',day:'numeric'}) + '</div>' +
        '<div class="tr-msg">' + (trial.message || 'للاستمرار في استخدام جميع المميزات، يرجى ترقية الاشتراك.') + '</div>' +
        '<div class="tr-btns">' +
          '<a href="https://wa.me/' + atob('MjAxMjI4MzcwODA5') + '?text=' + encodeURIComponent('أريد ترقية الاشتراك') + '" target="_blank" class="tr-btn tr-primary">ترقية الآن</a>' +
          '<button class="tr-btn tr-secondary" id="trial-close">لاحقاً</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(overlay);
    
    document.getElementById('trial-close').onclick = function() {
      localStorage.setItem('trial_dismissed', new Date().toDateString());
      overlay.remove();
    };
    
  }
  
  function removeBlockScreen() {
    var el = document.getElementById('system-blocked');
    if (el) el.remove();
  }
  
  // Run check after page loads
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(checkStatus, 1000);
    });
  } else {
    setTimeout(checkStatus, 1000);
  }
  // Recheck periodically
  setInterval(checkStatus, CHECK_INTERVAL);
})();
