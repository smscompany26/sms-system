// Trial Expiry Popup
(function() {
  const TRIAL_END = new Date('2026-03-01T23:59:59');
  const DISMISS_KEY = 'trial_popup_dismissed';
  
  function showTrialPopup() {
    const now = new Date();
    const diff = TRIAL_END - now;
    if (diff <= 0) return; // expired
    const days = Math.ceil(diff / (1000*60*60*24));
    if (days > 3) return; // only show when 3 days or less
    
    // Check if dismissed today
    const dismissed = localStorage.getItem(DISMISS_KEY);
    if (dismissed === new Date().toDateString()) return;
    
    const overlay = document.createElement('div');
    overlay.id = 'trial-overlay';
    overlay.innerHTML = `
      <style>
        #trial-overlay {
          position: fixed; inset: 0; z-index: 99999;
          background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
          display: flex; align-items: center; justify-content: center;
          animation: trialFadeIn 0.3s ease;
        }
        @keyframes trialFadeIn { from { opacity:0; } to { opacity:1; } }
        .trial-box {
          background: linear-gradient(135deg, #1a1a2e, #16213e);
          border: 1px solid rgba(108,60,233,0.4);
          border-radius: 20px;
          padding: 32px 28px;
          max-width: 400px; width: 90%;
          text-align: center;
          font-family: 'Cairo', sans-serif;
          direction: rtl;
          box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(108,60,233,0.15);
          animation: trialSlideUp 0.4s ease;
        }
        @keyframes trialSlideUp { from { transform: translateY(30px); opacity:0; } to { transform: translateY(0); opacity:1; } }
        .trial-icon { font-size: 48px; margin-bottom: 16px; }
        .trial-title { color: #fff; font-size: 20px; font-weight: 700; margin-bottom: 8px; }
        .trial-days {
          font-size: 52px; font-weight: 800;
          background: linear-gradient(135deg, #f85149, #ff6b6b);
          -webkit-background-clip: text; -webkit-text-fill-color: transparent;
          margin: 12px 0;
          line-height: 1;
        }
        .trial-subtitle { color: #a0a0b8; font-size: 14px; margin-bottom: 8px; line-height: 1.6; }
        .trial-msg { color: #8888a8; font-size: 12px; margin-bottom: 24px; line-height: 1.6; }
        .trial-btn-row { display: flex; gap: 10px; justify-content: center; }
        .trial-btn {
          padding: 12px 24px; border-radius: 12px; font-size: 14px; font-weight: 600;
          cursor: pointer; border: none; font-family: 'Cairo', sans-serif;
          transition: all 0.2s;
        }
        .trial-btn-primary {
          background: linear-gradient(135deg, #6c3ce9, #8b5cf6);
          color: #fff;
        }
        .trial-btn-primary:hover { transform: scale(1.03); box-shadow: 0 4px 20px rgba(108,60,233,0.4); }
        .trial-btn-secondary {
          background: rgba(255,255,255,0.08);
          color: #a0a0b8; border: 1px solid rgba(255,255,255,0.1);
        }
        .trial-btn-secondary:hover { background: rgba(255,255,255,0.12); }
        .trial-timer { color: #f85149; font-size: 11px; margin-top: 16px; font-family: monospace; }
      </style>
      <div class="trial-box">
        <div class="trial-icon">⏰</div>
        <div class="trial-title">الفترة التجريبية على وشك الانتهاء</div>
        <div class="trial-days">${days}</div>
        <div class="trial-subtitle">يوم متبقي على انتهاء الفترة التجريبية</div>
        <div class="trial-msg">للاستمرار في استخدام جميع المميزات بدون انقطاع،<br>يرجى ترقية الاشتراك قبل انتهاء الفترة التجريبية.</div>
        <div class="trial-btn-row">
          <button class="trial-btn trial-btn-primary" onclick="window.open('https://wa.me/201228370809?text=أريد ترقية اشتراك SMS System','_blank')">ترقية الآن</button>
          <button class="trial-btn trial-btn-secondary" id="trial-dismiss">لاحقاً</button>
        </div>
        <div class="trial-timer" id="trial-countdown"></div>
      </div>
    `;
    document.body.appendChild(overlay);
    
    document.getElementById('trial-dismiss').onclick = function() {
      localStorage.setItem(DISMISS_KEY, new Date().toDateString());
      overlay.style.animation = 'trialFadeIn 0.2s ease reverse';
      setTimeout(() => overlay.remove(), 200);
    };
    
    // Countdown timer
    function updateCountdown() {
      const now2 = new Date();
      const diff2 = TRIAL_END - now2;
      if (diff2 <= 0) return;
      const d = Math.floor(diff2/(1000*60*60*24));
      const h = Math.floor((diff2%(1000*60*60*24))/(1000*60*60));
      const m = Math.floor((diff2%(1000*60*60))/(1000*60));
      const s = Math.floor((diff2%(1000*60))/1000);
      const el = document.getElementById('trial-countdown');
      if (el) el.textContent = `${d} يوم : ${h} ساعة : ${m} دقيقة : ${s} ثانية`;
    }
    updateCountdown();
    setInterval(updateCountdown, 1000);
  }
  
  // Show after 2 seconds
  setTimeout(showTrialPopup, 2000);
})();
