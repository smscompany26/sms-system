// System Kill Switch — checks control panel status
(function() {
  const SYSTEM_ID = 'sms-system';
  const STATUS_URL = 'https://raw.githubusercontent.com/smscompany26/system-control/main/status.json';
  const CHECK_INTERVAL = 60000; // check every 60s
  
  async function checkStatus() {
    try {
      const res = await fetch(STATUS_URL + '?t=' + Date.now());
      if (!res.ok) return; // if can't reach, allow access
      const data = await res.json();
      const sys = data.systems && data.systems[SYSTEM_ID];
      if (!sys) return;
      
      const owner = data.owner || {};
      
      if (sys.status === 'disabled') {
        showBlockScreen(owner, 'permanent');
      } else if (sys.status === 'temp-disabled' && sys.disableUntil) {
        const until = new Date(sys.disableUntil);
        if (until > new Date()) {
          showBlockScreen(owner, 'temporary', until);
        }
      } else {
        removeBlockScreen();
      }
    } catch(e) {
      // Network error — don't block
    }
  }
  
  function showBlockScreen(owner, type, until) {
    if (document.getElementById('system-blocked')) return;
    
    const overlay = document.createElement('div');
    overlay.id = 'system-blocked';
    
    let countdownHTML = '';
    if (type === 'temporary' && until) {
      countdownHTML = `<div id="block-countdown" style="font-family:'JetBrains Mono',monospace;font-size:18px;color:#d29922;margin:16px 0;direction:ltr;"></div>
        <p style="color:#8888a8;font-size:13px;">سيتم إعادة تفعيل النظام تلقائياً بعد انتهاء المدة</p>`;
    }
    
    overlay.innerHTML = `
      <style>
        #system-blocked {
          position:fixed; inset:0; z-index:999999;
          background:linear-gradient(135deg, #0a0e14, #1a1a2e);
          display:flex; align-items:center; justify-content:center;
          font-family:'Cairo','Segoe UI',sans-serif; direction:rtl;
        }
        .block-box {
          text-align:center; max-width:450px; width:90%; padding:40px 30px;
        }
        .block-icon { font-size:64px; margin-bottom:20px; }
        .block-title { color:#f85149; font-size:24px; font-weight:700; margin-bottom:12px; }
        .block-msg { color:#a0a0b8; font-size:15px; line-height:1.8; margin-bottom:24px; }
        .block-contact {
          background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);
          border-radius:16px; padding:20px; margin-top:20px;
        }
        .block-contact-title { color:#e6edf3; font-size:14px; font-weight:600; margin-bottom:12px; }
        .block-contact a {
          display:inline-flex; align-items:center; gap:8px;
          padding:10px 20px; border-radius:10px; text-decoration:none;
          font-size:13px; font-weight:600; margin:4px;
          transition:all 0.2s;
        }
        .block-wa { background:rgba(37,211,102,0.15); color:#25d366; }
        .block-wa:hover { background:rgba(37,211,102,0.25); }
        .block-call { background:rgba(88,166,255,0.15); color:#58a6ff; }
        .block-call:hover { background:rgba(88,166,255,0.25); }
        .block-web { background:rgba(188,140,255,0.15); color:#bc8cff; }
        .block-web:hover { background:rgba(188,140,255,0.25); }
      </style>
      <div class="block-box">
        <div class="block-icon">🚫</div>
        <div class="block-title">${type === 'temporary' ? 'النظام معطّل مؤقتاً' : 'النظام معطّل'}</div>
        <div class="block-msg">
          ${type === 'temporary' 
            ? 'تم تعطيل النظام مؤقتاً من قبل المسؤول.<br>يرجى الانتظار أو التواصل مع المطور.'
            : 'تم تعطيل هذا النظام.<br>للاستفسار أو إعادة التفعيل، يرجى التواصل مع المطور.'}
        </div>
        ${countdownHTML}
        <div class="block-contact">
          <div class="block-contact-title">📞 تواصل مع المطور</div>
          <a href="https://wa.me/${(owner.whatsapp||'').replace('+','')}" target="_blank" class="block-wa">💬 واتساب</a>
          <a href="tel:${owner.phone||''}" class="block-call">📱 ${owner.phone||''}</a>
          ${owner.website ? `<a href="${owner.website}" target="_blank" class="block-web">🌐 الموقع</a>` : ''}
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    
    // Countdown for temp disable
    if (type === 'temporary' && until) {
      function updateCD() {
        const el = document.getElementById('block-countdown');
        if (!el) return;
        const diff = until - new Date();
        if (diff <= 0) { location.reload(); return; }
        const d = Math.floor(diff/86400000);
        const h = Math.floor((diff%86400000)/3600000);
        const m = Math.floor((diff%3600000)/60000);
        const s = Math.floor((diff%60000)/1000);
        el.textContent = `${d} يوم : ${String(h).padStart(2,'0')} ساعة : ${String(m).padStart(2,'0')} دقيقة : ${String(s).padStart(2,'0')} ثانية`;
      }
      updateCD();
      setInterval(updateCD, 1000);
    }
  }
  
  function removeBlockScreen() {
    const el = document.getElementById('system-blocked');
    if (el) el.remove();
  }
  
  // Check on load
  checkStatus();
  // Recheck periodically
  setInterval(checkStatus, CHECK_INTERVAL);
})();
