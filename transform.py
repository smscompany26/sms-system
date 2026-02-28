#!/usr/bin/env python3
"""
Transform SMS System index.html to add bilingual AR/EN support with LTR layout.
SAFETY: Only modifies UI text, CSS, and adds translation infrastructure.
Does NOT touch Supabase calls, business logic, or data handling.
"""

import re

with open('/tmp/sms-system/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Version bump v7.1.0 -> v7.2.0
content = content.replace('v7.1.0', 'v7.2.0')

# 2. Find the closing </style> tag (first one) to inject LTR CSS before it
ltr_css = """
/* ========== LTR Support ========== */
[dir="ltr"] .sidebar { right: auto; left: 0; border-right: 1px solid rgba(255,255,255,0.06); border-left: none; }
[dir="ltr"] .main-content { margin-right: 0; margin-left: 260px; }
[dir="ltr"] .sidebar.collapsed ~ .main-content { margin-left: 70px; margin-right: 0; }
[dir="ltr"] .stat-card { border-right: none; border-left: 4px solid var(--primary-light); }
[dir="ltr"] .stat-card.stat-sales { border-left-color: var(--success); border-right: none; }
[dir="ltr"] .stat-card.stat-purchases { border-left-color: var(--danger); border-right: none; }
[dir="ltr"] .stat-card.stat-profit { border-left-color: var(--primary); border-right: none; }
[dir="ltr"] .stat-card.stat-maintenance { border-left-color: var(--warning); border-right: none; }
[dir="ltr"] .nav-item i { margin-right: 10px; margin-left: 0; }
[dir="ltr"] .sidebar-nav { text-align: left; }
[dir="ltr"] .settings-nav-item > i:last-child { transform: rotate(180deg); }
[dir="ltr"] .settings-back i { transform: rotate(180deg); }
[dir="ltr"] .topbar { text-align: left; }
[dir="ltr"] .page-header { direction: ltr; }
[dir="ltr"] .form-row { direction: ltr; }
[dir="ltr"] .modal-header { direction: ltr; }
[dir="ltr"] .modal-footer { direction: ltr; }
[dir="ltr"] .search-box { direction: ltr; }
[dir="ltr"] .alert { direction: ltr; }
[dir="ltr"] .invoice-summary { direction: ltr; }
[dir="ltr"] .nav-arrow { margin-left: 0; margin-right: auto; }
[dir="ltr"] .sidebar-footer .btn-logout { margin-left: 0; margin-right: auto; }
[dir="ltr"] .mobile-bottom-nav { direction: ltr; }
[dir="ltr"] .mobile-more-menu { right: auto; left: 0; }
[dir="ltr"] .stat-card[style*="border-right-color"] { border-right: none !important; border-left: 4px solid var(--primary-light) !important; }
[dir="ltr"] .stat-card[style*="border-right-color:#f59e0b"] { border-left-color: #f59e0b !important; }
[dir="ltr"] .stat-card[style*="border-right-color:#6c3ce9"] { border-left-color: #6c3ce9 !important; }
[dir="ltr"] .stat-card[style*="border-right-color:#ef4444"] { border-left-color: #ef4444 !important; }
[dir="ltr"] .stat-card[style*="border-right-color:#22c55e"] { border-left-color: #22c55e !important; }
[dir="ltr"] .stat-card[style*="border-right-color:var(--accent)"] { border-left-color: var(--accent) !important; }
[dir="ltr"] .stat-card[style*="border-right-color:var(--primary)"] { border-left-color: var(--primary) !important; }
[dir="ltr"] .stat-card[style*="border-right-color:var(--warning)"] { border-left-color: var(--warning) !important; }
[dir="ltr"] .stat-card[style*="border-right-color:var(--danger)"] { border-left-color: var(--danger) !important; }
[dir="ltr"] .stat-card[style*="border-right-color:var(--success)"] { border-left-color: var(--success) !important; }
.lang-toggle { 
  background: rgba(108,60,233,0.1); color: var(--primary); border: 1px solid var(--primary); 
  padding: 4px 12px; border-radius: 20px; cursor: pointer; font-size: 13px; font-weight: 600;
  font-family: var(--font); transition: var(--transition); margin: 0 4px;
}
.lang-toggle:hover { background: var(--primary); color: #fff; }
@media(max-width:768px) {
  [dir="ltr"] .main-content { margin-left: 0; }
  [dir="ltr"] .sidebar.mobile-open { left: 0; right: auto; }
}
"""

# Insert LTR CSS before first </style>
content = content.replace('</style>', ltr_css + '</style>', 1)

# 3. Add language toggle button in topbar
content = content.replace(
    '<button class="theme-toggle" id="theme-toggle" onclick="toggleTheme()" title="الوضع الليلي"><i class=\'bx bx-moon\'></i></button>',
    '<button class="lang-toggle" id="lang-toggle" onclick="toggleLanguage()">EN</button>\n        <button class="theme-toggle" id="theme-toggle" onclick="toggleTheme()" title="الوضع الليلي"><i class=\'bx bx-moon\'></i></button>'
)

# 4. Add data-i18n attributes to static HTML elements
# Sidebar nav items
replacements = [
    # Sidebar items
    ("<i class='bx bxs-dashboard'></i><span>لوحة التحكم</span>", "<i class='bx bxs-dashboard'></i><span data-i18n=\"nav_dashboard\">لوحة التحكم</span>"),
    ("<i class='bx bxs-package'></i><span>المخزون</span>", "<i class='bx bxs-package'></i><span data-i18n=\"nav_inventory\">المخزون</span>"),
    ("<i class='bx bxs-cart'></i><span>البيع</span>", "<i class='bx bxs-cart'></i><span data-i18n=\"nav_sales\">البيع</span>"),
    ("<i class='bx bxs-cart-download'></i><span>المشتريات</span>", "<i class='bx bxs-cart-download'></i><span data-i18n=\"nav_purchases\">المشتريات</span>"),
    ("<i class='bx bxs-wrench'></i><span>ورشة الصيانة</span>", "<i class='bx bxs-wrench'></i><span data-i18n=\"nav_maintenance\">ورشة الصيانة</span>"),
    ("<i class='bx bxs-wallet'></i><span>المحاسبة</span>", "<i class='bx bxs-wallet'></i><span data-i18n=\"nav_accounting\">المحاسبة</span>"),
    ("<i class='bx bxs-report'></i><span>التقارير</span>", "<i class='bx bxs-report'></i><span data-i18n=\"nav_reports\">التقارير</span>"),
    ("<i class='bx bxs-cog'></i><span>الإعدادات</span>", "<i class='bx bxs-cog'></i><span data-i18n=\"nav_settings\">الإعدادات</span>"),
    
    # Sidebar sub items
    ('onclick="navigate(\'inventory\');setTimeout(()=>{},100)">المنتجات</a>', 'onclick="navigate(\'inventory\');setTimeout(()=>{},100)" data-i18n="nav_products">المنتجات</a>'),
    ('onclick="navigate(\'categories\')">التصنيفات</a>', 'onclick="navigate(\'categories\')" data-i18n="nav_categories">التصنيفات</a>'),
    ('onclick="navigate(\'inventory\');setTimeout(openImportExport,100)">استيراد / تصدير</a>', 'onclick="navigate(\'inventory\');setTimeout(openImportExport,100)" data-i18n="nav_import_export">استيراد / تصدير</a>'),
    ("onclick=\"navigate('sales');setTimeout(()=>switchSalesTab('invoices'),100)\">الفواتير</a>", "onclick=\"navigate('sales');setTimeout(()=>switchSalesTab('invoices'),100)\" data-i18n=\"nav_invoices\">الفواتير</a>"),
    ("onclick=\"navigate('sales');setTimeout(()=>switchSalesTab('clients'),100)\">العملاء</a>", "onclick=\"navigate('sales');setTimeout(()=>switchSalesTab('clients'),100)\" data-i18n=\"nav_clients\">العملاء</a>"),
    ("onclick=\"navigate('purchases');setTimeout(()=>switchPurchasesTab('invoices'),100)\">الفواتير</a>", "onclick=\"navigate('purchases');setTimeout(()=>switchPurchasesTab('invoices'),100)\" data-i18n=\"nav_invoices\">الفواتير</a>"),
    ("onclick=\"navigate('purchases');setTimeout(()=>switchPurchasesTab('suppliers'),100)\">الموردين</a>", "onclick=\"navigate('purchases');setTimeout(()=>switchPurchasesTab('suppliers'),100)\" data-i18n=\"nav_suppliers\">الموردين</a>"),
    ("onclick=\"navigate('accounting')\">الملخص</a>", "onclick=\"navigate('accounting')\" data-i18n=\"nav_summary\">الملخص</a>"),
    # accounting expenses sub
    ("""onclick="navigate('accounting');setTimeout(()=>document.getElementById('expenses-table')?.scrollIntoView({behavior:'smooth'}),200)">المصروفات</a>""",
     """onclick="navigate('accounting');setTimeout(()=>document.getElementById('expenses-table')?.scrollIntoView({behavior:'smooth'}),200)" data-i18n="nav_expenses">المصروفات</a>"""),
    # Reports sub
    ("onclick=\"navigate('reports');setTimeout(()=>switchReportTab('daily'),100)\">يومي</a>", "onclick=\"navigate('reports');setTimeout(()=>switchReportTab('daily'),100)\" data-i18n=\"nav_daily\">يومي</a>"),
    ("onclick=\"navigate('reports');setTimeout(()=>switchReportTab('monthly'),100)\">شهري</a>", "onclick=\"navigate('reports');setTimeout(()=>switchReportTab('monthly'),100)\" data-i18n=\"nav_monthly\">شهري</a>"),
    ("onclick=\"navigate('reports');setTimeout(()=>switchReportTab('inventory'),100)\">المخزون</a>", "onclick=\"navigate('reports');setTimeout(()=>switchReportTab('inventory'),100)\" data-i18n=\"nav_inventory_report\">المخزون</a>"),
    ("onclick=\"navigate('reports');setTimeout(()=>switchReportTab('outstanding'),100)\">المستحقات</a>", "onclick=\"navigate('reports');setTimeout(()=>switchReportTab('outstanding'),100)\" data-i18n=\"nav_outstanding\">المستحقات</a>"),
    # Settings sub
    ("onclick=\"navigate('settings')\">الرئيسية</a>", "onclick=\"navigate('settings')\" data-i18n=\"nav_main\">الرئيسية</a>"),
    ("onclick=\"navigate('settings','company')\">بيانات الشركة</a>", "onclick=\"navigate('settings','company')\" data-i18n=\"nav_company\">بيانات الشركة</a>"),
    ("onclick=\"navigate('settings','notifications')\">الإشعارات</a>", "onclick=\"navigate('settings','notifications')\" data-i18n=\"nav_notifications\">الإشعارات</a>"),
    ("onclick=\"navigate('settings','drive')\">المزامنة السحابية</a>", "onclick=\"navigate('settings','drive')\" data-i18n=\"nav_cloud_sync\">المزامنة السحابية</a>"),
    ("onclick=\"navigate('settings','backup')\">النسخ الاحتياطي</a>", "onclick=\"navigate('settings','backup')\" data-i18n=\"nav_backup\">النسخ الاحتياطي</a>"),
    ("onclick=\"navigate('settings','users')\">فريق العمل</a>", "onclick=\"navigate('settings','users')\" data-i18n=\"nav_team\">فريق العمل</a>"),
    ("onclick=\"navigate('settings','activity')\">سجل النشاط</a>", "onclick=\"navigate('settings','activity')\" data-i18n=\"nav_activity\">سجل النشاط</a>"),
    
    # Dashboard stat labels
    ('<span class="stat-label">مبيعات اليوم</span>', '<span class="stat-label" data-i18n="stat_sales_today">مبيعات اليوم</span>'),
    ('<span class="stat-label">مشتريات اليوم</span>', '<span class="stat-label" data-i18n="stat_purchases_today">مشتريات اليوم</span>'),
    ('<span class="stat-label">صافي الربح</span>', '<span class="stat-label" data-i18n="stat_net_profit">صافي الربح</span>'),
    ('<span class="stat-label">أجهزة تحت الصيانة</span>', '<span class="stat-label" data-i18n="stat_under_maintenance">أجهزة تحت الصيانة</span>'),
    ('<span class="stat-label">إجمالي المنتجات</span>', '<span class="stat-label" data-i18n="stat_total_products">إجمالي المنتجات</span>'),
    ('<span class="stat-label">إجمالي العملاء</span>', '<span class="stat-label" data-i18n="stat_total_clients">إجمالي العملاء</span>'),
    ('<span class="stat-label">إجمالي الموردين</span>', '<span class="stat-label" data-i18n="stat_total_suppliers">إجمالي الموردين</span>'),
    ('<span class="stat-label">أجهزة نشطة</span>', '<span class="stat-label" data-i18n="stat_active_devices">أجهزة نشطة</span>'),
    
    # Dashboard section titles
    ('<div class="sales-widget-title"><i class=\'bx bx-bar-chart-alt-2\'></i> نظرة عامة على المبيعات</div>',
     '<div class="sales-widget-title"><i class=\'bx bx-bar-chart-alt-2\'></i> <span data-i18n="sales_overview">نظرة عامة على المبيعات</span></div>'),
    ('<span class="summary-label">المبيعات</span>', '<span class="summary-label" data-i18n="label_sales">المبيعات</span>'),
    ('<span class="summary-label">المشتريات</span>', '<span class="summary-label" data-i18n="label_purchases">المشتريات</span>'),
    ('<span class="summary-label">صافي الربح</span>', '<span class="summary-label" data-i18n="stat_net_profit">صافي الربح</span>'),
    
    # Period tabs
    ("onclick=\"switchSalesPeriod('week')\">أسبوع</button>", "onclick=\"switchSalesPeriod('week')\" data-i18n=\"period_week\">أسبوع</button>"),
    ("onclick=\"switchSalesPeriod('month')\">شهر</button>", "onclick=\"switchSalesPeriod('month')\" data-i18n=\"period_month\">شهر</button>"),
    ("onclick=\"switchSalesPeriod('year')\">سنة</button>", "onclick=\"switchSalesPeriod('year')\" data-i18n=\"period_year\">سنة</button>"),
    
    # Dashboard cards
    ('<h4><i class=\'bx bx-pie-chart-alt\'></i> حالة الصيانة</h4>', '<h4><i class=\'bx bx-pie-chart-alt\'></i> <span data-i18n="maint_status">حالة الصيانة</span></h4>'),
    ('<h4><i class=\'bx bx-trophy\'></i> أكثر 5 منتجات مبيعاً</h4>', '<h4><i class=\'bx bx-trophy\'></i> <span data-i18n="top_5_products">أكثر 5 منتجات مبيعاً</span></h4>'),
    ('<h4><i class=\'bx bx-line-chart\'></i> إيرادات آخر 6 شهور</h4>', '<h4><i class=\'bx bx-line-chart\'></i> <span data-i18n="revenue_6_months">إيرادات آخر 6 شهور</span></h4>'),
    
    # Alerts & Recent
    ('<h3><i class=\'bx bx-bell\'></i> تنبيهات</h3>', '<h3><i class=\'bx bx-bell\'></i> <span data-i18n="alerts">تنبيهات</span></h3>'),
    ('<p class="empty-state">لا توجد تنبيهات</p>', '<p class="empty-state" data-i18n="no_alerts">لا توجد تنبيهات</p>'),
    ('<h3><i class=\'bx bx-receipt\'></i> آخر الفواتير</h3>', '<h3><i class=\'bx bx-receipt\'></i> <span data-i18n="recent_invoices">آخر الفواتير</span></h3>'),
    ('<p class="empty-state">لا توجد فواتير</p>', '<p class="empty-state" data-i18n="no_invoices">لا توجد فواتير</p>'),
    ('<h3><i class=\'bx bx-history\'></i> آخر الحركات</h3>', '<h3><i class=\'bx bx-history\'></i> <span data-i18n="recent_activity">آخر الحركات</span></h3>'),
    
    # Activity tabs
    ("onclick=\"switchActivityTab('operations')\">العمليات</button>", "onclick=\"switchActivityTab('operations')\" data-i18n=\"tab_operations\">العمليات</button>"),
    ("onclick=\"switchActivityTab('logins')\">تسجيل الدخول</button>", "onclick=\"switchActivityTab('logins')\" data-i18n=\"tab_logins\">تسجيل الدخول</button>"),
    ('<p class="empty-state">لا توجد حركات</p>', '<p class="empty-state" data-i18n="no_activity">لا توجد حركات</p>'),
    ('<i class=\'bx bx-list-ul\'></i> عرض كل الحركات', '<i class=\'bx bx-list-ul\'></i> <span data-i18n="show_all_activity">عرض كل الحركات</span>'),
    
    # Quick Actions
    ('<h3><i class=\'bx bx-rocket\'></i> إجراءات سريعة</h3>', '<h3><i class=\'bx bx-rocket\'></i> <span data-i18n="quick_actions">إجراءات سريعة</span></h3>'),
    ("<i class='bx bx-plus-circle'></i> إضافة صنف</button>", "<i class='bx bx-plus-circle'></i> <span data-i18n=\"add_product\">إضافة صنف</span></button>"),
    ("<i class='bx bx-receipt'></i> فاتورة بيع</button>", "<i class='bx bx-receipt'></i> <span data-i18n=\"sale_invoice\">فاتورة بيع</span></button>"),
    ("<i class='bx bx-cart-download'></i> فاتورة شراء</button>", "<i class='bx bx-cart-download'></i> <span data-i18n=\"purchase_invoice\">فاتورة شراء</span></button>"),
    ("<i class='bx bx-wrench'></i> إذن صيانة</button>", "<i class='bx bx-wrench'></i> <span data-i18n=\"maint_order\">إذن صيانة</span></button>"),
    
    # Inventory page
    ('placeholder="بحث بالاسم أو الكود..."', 'placeholder="بحث بالاسم أو الكود..." data-i18n-placeholder="search_name_code"'),
    ('<option value="">كل التصنيفات</option>', '<option value="" data-i18n="all_categories">كل التصنيفات</option>'),
    ('<option value="new">جديد</option>', '<option value="new" data-i18n="cond_new">جديد</option>'),
    ('<option value="used">مستعمل</option>', '<option value="used" data-i18n="cond_used">مستعمل</option>'),
    ('<option value="device">جهاز</option>', '<option value="device" data-i18n="type_device">جهاز</option>'),
    ('<option value="part">قطعة غيار</option>', '<option value="part" data-i18n="type_part">قطعة غيار</option>'),
    ("<i class='bx bx-barcode'></i> مسح باركود</button>", "<i class='bx bx-barcode'></i> <span data-i18n=\"scan_barcode\">مسح باركود</span></button>"),
    ("<i class='bx bx-plus'></i> إضافة صنف</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_product\">إضافة صنف</span></button>"),
    ("<i class='bx bx-import'></i> استيراد/تصدير</button>", "<i class='bx bx-import'></i> <span data-i18n=\"import_export\">استيراد/تصدير</span></button>"),
    ("<i class='bx bx-category'></i> التصنيفات</button>", "<i class='bx bx-category'></i> <span data-i18n=\"nav_categories\">التصنيفات</span></button>"),
    
    # Products table headers
    ('<th>الكود</th>\n                  <th>الصنف</th>\n                  <th>الحالة</th>\n                  <th>النوع</th>\n                  <th>التصنيف</th>\n                  <th>سعر الشراء</th>\n                  <th>سعر البيع</th>\n                  <th>الكمية</th>\n                  <th>الحد الأدنى</th>\n                  <th>إجراءات</th>',
     '<th data-i18n="th_code">الكود</th>\n                  <th data-i18n="th_product">الصنف</th>\n                  <th data-i18n="th_condition">الحالة</th>\n                  <th data-i18n="th_type">النوع</th>\n                  <th data-i18n="th_category">التصنيف</th>\n                  <th data-i18n="th_buy_price">سعر الشراء</th>\n                  <th data-i18n="th_sell_price">سعر البيع</th>\n                  <th data-i18n="th_quantity">الكمية</th>\n                  <th data-i18n="th_min_stock">الحد الأدنى</th>\n                  <th data-i18n="th_actions">إجراءات</th>'),
    
    # Low stock alert
    ('أصناف وصلت للحد الأدنى!', '<span data-i18n="low_stock_alert">أصناف وصلت للحد الأدنى!</span>'),
    ("onclick=\"showLowStock()\">عرض</button>", "onclick=\"showLowStock()\" data-i18n=\"btn_show\">عرض</button>"),
    
    # Empty states
    ('<p>لا توجد أصناف بعد</p>', '<p data-i18n="no_products">لا توجد أصناف بعد</p>'),
    
    # Sales page tabs
    ("onclick=\"switchSalesTab('invoices')\">الفواتير</button>", "onclick=\"switchSalesTab('invoices')\" data-i18n=\"tab_invoices\">الفواتير</button>"),
    ("onclick=\"switchSalesTab('clients')\">العملاء</button>", "onclick=\"switchSalesTab('clients')\" data-i18n=\"tab_clients\">العملاء</button>"),
    ("onclick=\"switchSalesTab('services')\">خدمات وزيارات</button>", "onclick=\"switchSalesTab('services')\" data-i18n=\"tab_services\">خدمات وزيارات</button>"),
    
    # Purchases tabs
    ("onclick=\"switchPurchasesTab('invoices')\">الفواتير</button>", "onclick=\"switchPurchasesTab('invoices')\" data-i18n=\"tab_invoices\">الفواتير</button>"),
    ("onclick=\"switchPurchasesTab('suppliers')\">الموردين</button>", "onclick=\"switchPurchasesTab('suppliers')\" data-i18n=\"tab_suppliers\">الموردين</button>"),
    
    # Maintenance tabs
    ("onclick=\"switchMaintenanceTab('devices')\">أجهزة</button>", "onclick=\"switchMaintenanceTab('devices')\" data-i18n=\"tab_devices\">أجهزة</button>"),
    ("onclick=\"switchMaintenanceTab('visits')\">زيارات وخدمات</button>", "onclick=\"switchMaintenanceTab('visits')\" data-i18n=\"tab_visits\">زيارات وخدمات</button>"),
    
    # Maintenance stats
    ('<span class="stat-label">تحت الصيانة</span>', '<span class="stat-label" data-i18n="stat_under_repair">تحت الصيانة</span>'),
    ('<span class="stat-label">خلصت ومتسلمتش</span>', '<span class="stat-label" data-i18n="stat_done_not_delivered">خلصت ومتسلمتش</span>'),
    ('<span class="stat-label">اتسلمت ومدفعتش</span>', '<span class="stat-label" data-i18n="stat_delivered_not_paid">اتسلمت ومدفعتش</span>'),
    ('<span class="stat-label">مكتملة</span>', '<span class="stat-label" data-i18n="stat_completed">مكتملة</span>'),
    
    # Search placeholders
    ('placeholder="بحث بالاسم أو رقم الأمر..."', 'placeholder="بحث بالاسم أو رقم الأمر..." data-i18n-placeholder="search_name_order"'),
    ("onclick=\"filterDevicesByStatus('all')\">الكل</button>", "onclick=\"filterDevicesByStatus('all')\" data-i18n=\"filter_all\">الكل</button>"),
    ("<i class='bx bx-plus'></i> إذن استلام جهاز</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"new_device_intake\">إذن استلام جهاز</span></button>"),
    
    # Accounting
    ('<span class="stat-label">إجمالي الإيرادات</span>', '<span class="stat-label" data-i18n="stat_total_revenue">إجمالي الإيرادات</span>'),
    ('<span class="stat-label">إجمالي المصروفات</span>', '<span class="stat-label" data-i18n="stat_total_expenses">إجمالي المصروفات</span>'),
    ('<span class="stat-label">مبالغ مستحقة من العملاء</span>', '<span class="stat-label" data-i18n="stat_owed_by_clients">مبالغ مستحقة من العملاء</span>'),
    ('<h3><i class=\'bx bx-user\'></i> أرصدة العملاء (مين عليه فلوس)</h3>', '<h3><i class=\'bx bx-user\'></i> <span data-i18n="client_balances">أرصدة العملاء (مين عليه فلوس)</span></h3>'),
    ('<h3><i class=\'bx bx-store\'></i> أرصدة الموردين (مين لينا عنده فلوس)</h3>', '<h3><i class=\'bx bx-store\'></i> <span data-i18n="supplier_balances">أرصدة الموردين (مين لينا عنده فلوس)</span></h3>'),
    ('<h3 style="margin:0"><i class=\'bx bx-money\'></i> المصروفات</h3>', '<h3 style="margin:0"><i class=\'bx bx-money\'></i> <span data-i18n="expenses">المصروفات</span></h3>'),
    ("<i class='bx bx-plus'></i> إضافة مصروف</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_expense\">إضافة مصروف</span></button>"),
    
    # Expense tabs
    ("onclick=\"switchExpenseTab('treasury')\">مصروفات خزينة</button>", "onclick=\"switchExpenseTab('treasury')\" data-i18n=\"tab_treasury\">مصروفات خزينة</button>"),
    ("onclick=\"switchExpenseTab('indirect')\">مصروفات غير مباشرة</button>", "onclick=\"switchExpenseTab('indirect')\" data-i18n=\"tab_indirect\">مصروفات غير مباشرة</button>"),
    ("onclick=\"switchExpenseTab('all')\">الكل</button>", "onclick=\"switchExpenseTab('all')\" data-i18n=\"tab_all\">الكل</button>"),
    ('<span class="stat-label">إجمالي مصروفات الخزينة</span>', '<span class="stat-label" data-i18n="stat_treasury_total">إجمالي مصروفات الخزينة</span>'),
    ('<span class="stat-label">إجمالي المصروفات غير المباشرة</span>', '<span class="stat-label" data-i18n="stat_indirect_total">إجمالي المصروفات غير المباشرة</span>'),
    
    # Reports tabs
    ("onclick=\"switchReportTab('daily')\">يومي</button>", "onclick=\"switchReportTab('daily')\" data-i18n=\"tab_daily\">يومي</button>"),
    ("onclick=\"switchReportTab('monthly')\">شهري</button>", "onclick=\"switchReportTab('monthly')\" data-i18n=\"tab_monthly\">شهري</button>"),
    ("onclick=\"switchReportTab('inventory')\">المخزون</button>", "onclick=\"switchReportTab('inventory')\" data-i18n=\"tab_inventory\">المخزون</button>"),
    ("onclick=\"switchReportTab('outstanding')\">المستحقات</button>", "onclick=\"switchReportTab('outstanding')\" data-i18n=\"tab_outstanding\">المستحقات</button>"),
    ("<i class='bx bx-printer'></i> طباعة / PDF</button>", "<i class='bx bx-printer'></i> <span data-i18n=\"print_pdf\">طباعة / PDF</span></button>"),
    
    # Settings
    ('<span class="stat-label">الشركة</span>', '<span class="stat-label" data-i18n="label_company">الشركة</span>'),
    ('<span class="stat-label">المزامنة السحابية</span>', '<span class="stat-label" data-i18n="label_cloud_sync">المزامنة السحابية</span>'),
    ('<span class="stat-label">فريق العمل</span>', '<span class="stat-label" data-i18n="label_team">فريق العمل</span>'),
    ('<span class="stat-label">إصدار النظام</span>', '<span class="stat-label" data-i18n="label_version">إصدار النظام</span>'),
    
    # User role badge
    ('<span class="user-role-badge" id="user-role-badge">مدير</span>', '<span class="user-role-badge" id="user-role-badge" data-i18n="role_admin">مدير</span>'),
    
    # Mobile bottom nav
    ("<i class='bx bxs-dashboard'></i>الرئيسية</button>", "<i class='bx bxs-dashboard'></i><span data-i18n=\"nav_home\">الرئيسية</span></button>"),
    ("<i class='bx bxs-package'></i>المخزون</button>", "<i class='bx bxs-package'></i><span data-i18n=\"nav_inventory\">المخزون</span></button>"),
    ("<i class='bx bxs-cart'></i>البيع</button>", "<i class='bx bxs-cart'></i><span data-i18n=\"nav_sales\">البيع</span></button>"),
    ("<i class='bx bxs-wrench'></i>الصيانة</button>", "<i class='bx bxs-wrench'></i><span data-i18n=\"nav_maintenance_short\">الصيانة</span></button>"),
    ("<i class='bx bx-menu'></i>المزيد</button>", "<i class='bx bx-menu'></i><span data-i18n=\"nav_more\">المزيد</span></button>"),
    ("<i class='bx bxs-cart-download'></i> المشتريات</a>", "<i class='bx bxs-cart-download'></i> <span data-i18n=\"nav_purchases\">المشتريات</span></a>"),
    ("<i class='bx bxs-wallet'></i> المحاسبة</a>", "<i class='bx bxs-wallet'></i> <span data-i18n=\"nav_accounting\">المحاسبة</span></a>"),
    ("<i class='bx bxs-report'></i> التقارير</a>", "<i class='bx bxs-report'></i> <span data-i18n=\"nav_reports\">التقارير</span></a>"),
    ("<i class='bx bxs-cog'></i> الإعدادات</a>", "<i class='bx bxs-cog'></i> <span data-i18n=\"nav_settings\">الإعدادات</span></a>"),
    ("<i class='bx bx-log-out'></i> تسجيل الخروج</a>", "<i class='bx bx-log-out'></i> <span data-i18n=\"logout\">تسجيل الخروج</span></a>"),
    
    # Search placeholders  
    ('placeholder="بحث في الفواتير..."', 'placeholder="بحث في الفواتير..." data-i18n-placeholder="search_invoices"'),
    ('placeholder="بحث في العملاء..."', 'placeholder="بحث في العملاء..." data-i18n-placeholder="search_clients"'),
    ('placeholder="بحث في الخدمات..."', 'placeholder="بحث في الخدمات..." data-i18n-placeholder="search_services"'),
    ('placeholder="بحث في الموردين..."', 'placeholder="بحث في الموردين..." data-i18n-placeholder="search_suppliers"'),
    ('placeholder="بحث في الزيارات..."', 'placeholder="بحث في الزيارات..." data-i18n-placeholder="search_visits"'),
    ('placeholder="بحث في التصنيفات..."', 'placeholder="بحث في التصنيفات..." data-i18n-placeholder="search_categories"'),
    
    # Buttons
    ("<i class='bx bx-plus'></i> فاتورة بيع جديدة</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"new_sale_invoice\">فاتورة بيع جديدة</span></button>"),
    ("<i class='bx bx-plus'></i> إضافة عميل</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_client\">إضافة عميل</span></button>"),
    ("<i class='bx bx-plus'></i> زيارة/خدمة جديدة</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"new_service\">زيارة/خدمة جديدة</span></button>"),
    ("<i class='bx bx-plus'></i> فاتورة شراء جديدة</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"new_purchase_invoice\">فاتورة شراء جديدة</span></button>"),
    ("<i class='bx bx-plus'></i> إضافة مورد</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_supplier\">إضافة مورد</span></button>"),
    ("<i class='bx bx-plus'></i> زيارة جديدة</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"new_visit\">زيارة جديدة</span></button>"),
    ("<i class='bx bx-plus'></i> إضافة تصنيف</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_category\">إضافة تصنيف</span></button>"),
    ("<i class='bx bx-plus'></i> إضافة مستخدم</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_user\">إضافة مستخدم</span></button>"),
    ("<i class='bx bx-plus'></i> إضافة مهندس/فني</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_engineer\">إضافة مهندس/فني</span></button>"),
    ("<i class='bx bx-plus'></i> إضافة مستلم</button>", "<i class='bx bx-plus'></i> <span data-i18n=\"add_recipient\">إضافة مستلم</span></button>"),
    
    # Empty states
    ('<p>لا يوجد عملاء</p>', '<p data-i18n="no_clients">لا يوجد عملاء</p>'),
    ('<p>لا توجد زيارات أو خدمات</p>', '<p data-i18n="no_services">لا توجد زيارات أو خدمات</p>'),
    ('<p>لا توجد فواتير شراء</p>', '<p data-i18n="no_purchase_invoices">لا توجد فواتير شراء</p>'),
    ('<p>لا يوجد موردين</p>', '<p data-i18n="no_suppliers">لا يوجد موردين</p>'),
    ('<p>لا توجد أجهزة في الصيانة</p>', '<p data-i18n="no_devices">لا توجد أجهزة في الصيانة</p>'),
    ('<p>لا توجد زيارات</p>', '<p data-i18n="no_visits">لا توجد زيارات</p>'),
    ('<p>لا توجد فواتير بيع</p>', '<p data-i18n="no_sale_invoices">لا توجد فواتير بيع</p>'),
    ('<p>لا توجد تصنيفات بعد</p>', '<p data-i18n="no_categories">لا توجد تصنيفات بعد</p>'),
    ('<p>لا يوجد مهندسين أو فنيين</p>', '<p data-i18n="no_engineers">لا يوجد مهندسين أو فنيين</p>'),
    ('<p>لا يوجد مستلمين — أضف Chat ID لبدء الإشعارات</p>', '<p data-i18n="no_recipients">لا يوجد مستلمين — أضف Chat ID لبدء الإشعارات</p>'),
    
    # Modal titles
    ('<h3 id="modal-product-title">إضافة صنف جديد</h3>', '<h3 id="modal-product-title" data-i18n="modal_add_product">إضافة صنف جديد</h3>'),
    ('<h3>إدارة التصنيفات</h3>', '<h3 data-i18n="modal_manage_categories">إدارة التصنيفات</h3>'),
    ('<h3 id="modal-stock-title">إضافة للمخزون</h3>', '<h3 id="modal-stock-title" data-i18n="modal_stock_in">إضافة للمخزون</h3>'),
    ('<h3>استيراد / تصدير المخزون</h3>', '<h3 data-i18n="modal_import_export">استيراد / تصدير المخزون</h3>'),
    ('<h3>تفاصيل الصنف</h3>', '<h3 data-i18n="modal_product_details">تفاصيل الصنف</h3>'),
    ('<h3>إضافة مصروف</h3>', '<h3 data-i18n="modal_add_expense">إضافة مصروف</h3>'),
    ('<h3 id="modal-user-title">إضافة مستخدم</h3>', '<h3 id="modal-user-title" data-i18n="modal_add_user">إضافة مستخدم</h3>'),
    ('<h3 id="modal-engineer-title">إضافة مهندس/فني</h3>', '<h3 id="modal-engineer-title" data-i18n="modal_add_engineer">إضافة مهندس/فني</h3>'),
    ('<h3 id="modal-device-title">إذن استلام جهاز جديد</h3>', '<h3 id="modal-device-title" data-i18n="modal_new_device">إذن استلام جهاز جديد</h3>'),
    ('<h3 id="modal-client-title">إضافة عميل جديد</h3>', '<h3 id="modal-client-title" data-i18n="modal_add_client">إضافة عميل جديد</h3>'),
    ('<h3 id="repair-history-title">تاريخ الصيانة</h3>', '<h3 id="repair-history-title" data-i18n="modal_repair_history">تاريخ الصيانة</h3>'),
    ('<h3 id="modal-supplier-title">إضافة مورد جديد</h3>', '<h3 id="modal-supplier-title" data-i18n="modal_add_supplier">إضافة مورد جديد</h3>'),
    ('<h3 id="modal-invoice-title">فاتورة جديدة</h3>', '<h3 id="modal-invoice-title" data-i18n="modal_new_invoice">فاتورة جديدة</h3>'),
    ('<h3 id="modal-recipient-title">إضافة مستلم</h3>', '<h3 id="modal-recipient-title" data-i18n="modal_add_recipient">إضافة مستلم</h3>'),
    ('<h3 id="modal-service-title">زيارة/خدمة جديدة</h3>', '<h3 id="modal-service-title" data-i18n="modal_new_service">زيارة/خدمة جديدة</h3>'),
    ('<h3 id="modal-adjust-balance-title">سجل المدفوعات</h3>', '<h3 id="modal-adjust-balance-title" data-i18n="modal_payment_ledger">سجل المدفوعات</h3>'),
    
    # Form labels in product modal
    ('<label>كود الصنف (SKU)</label>', '<label data-i18n="label_sku">كود الصنف (SKU)</label>'),
    ('<label>اسم الصنف *</label>', '<label data-i18n="label_product_name">اسم الصنف *</label>'),
    ('<label>الحالة *</label>', '<label data-i18n="label_condition">الحالة *</label>'),
    ('<label>النوع *</label>', '<label data-i18n="label_type">النوع *</label>'),
    ('<label>التصنيف</label>\n          <select id="product-category">', '<label data-i18n="label_category">التصنيف</label>\n          <select id="product-category">'),
    ('<option value="">بدون تصنيف</option>', '<option value="" data-i18n="no_category">بدون تصنيف</option>'),
    ('<label>سعر الشراء (ج.م) *</label>', '<label data-i18n="label_buy_price">سعر الشراء (ج.م) *</label>'),
    ('<label>سعر البيع (ج.م) *</label>', '<label data-i18n="label_sell_price">سعر البيع (ج.م) *</label>'),
    ('<label>الكمية *</label>\n          <input type="number" id="product-qty"', '<label data-i18n="label_quantity">الكمية *</label>\n          <input type="number" id="product-qty"'),
    ('<label>الحد الأدنى للمخزون</label>', '<label data-i18n="label_min_stock">الحد الأدنى للمخزون</label>'),
    ('<label>باركود</label>', '<label data-i18n="label_barcode">باركود</label>'),
    ('<label>الوصف</label>\n        <textarea id="product-description"', '<label data-i18n="label_description">الوصف</label>\n        <textarea id="product-description"'),
    ('<label>صورة</label>\n        <input type="file" id="product-image"', '<label data-i18n="label_image">صورة</label>\n        <input type="file" id="product-image"'),
    
    # Common button labels
    # Settings back
    ("<i class='bx bx-arrow-right'></i> رجوع</div>", "<i class='bx bx-arrow-right'></i> <span data-i18n=\"btn_back\">رجوع</span></div>"),
    
    # Chart labels
    ('<div class="chart-section-title" style="margin:0;"><i class=\'bx bx-chart\'></i> تفاصيل الفترة</div>',
     '<div class="chart-section-title" style="margin:0;"><i class=\'bx bx-chart\'></i> <span data-i18n="period_details">تفاصيل الفترة</span></div>'),
    
    # Settings section titles
    ('<h3><i class=\'bx bx-building\'></i> بيانات الشركة</h3>', '<h3><i class=\'bx bx-building\'></i> <span data-i18n="settings_company">بيانات الشركة</span></h3>'),
    ('<label>اسم الشركة</label>', '<label data-i18n="label_company_name">اسم الشركة</label>'),
    ('<label>التليفون</label><input type="tel" id="company-phone"', '<label data-i18n="label_phone">التليفون</label><input type="tel" id="company-phone"'),
    ('<label>العنوان</label><input type="text" id="company-address">', '<label data-i18n="label_address">العنوان</label><input type="text" id="company-address">'),
    ('<label>الرقم الضريبي</label>', '<label data-i18n="label_tax_number">الرقم الضريبي</label>'),
    ('<label>نسبة الضريبة %</label>', '<label data-i18n="label_vat_rate">نسبة الضريبة %</label>'),
    ('<label>اللوجو</label>', '<label data-i18n="label_logo">اللوجو</label>'),
    ("<i class='bx bx-save'></i> حفظ</button>", "<i class='bx bx-save'></i> <span data-i18n=\"btn_save\">حفظ</span></button>"),
    
    # Notifications section
    ('<h3><i class=\'bx bx-bot\'></i> إعدادات Telegram Bot</h3>', '<h3><i class=\'bx bx-bot\'></i> <span data-i18n="settings_telegram">إعدادات Telegram Bot</span></h3>'),
    ('<h3 style="margin:0"><i class=\'bx bx-bell\'></i> المستلمين</h3>', '<h3 style="margin:0"><i class=\'bx bx-bell\'></i> <span data-i18n="recipients">المستلمين</span></h3>'),
    
    # Cloud sync
    ('<h3><i class=\'bx bx-cloud\'></i> المزامنة السحابية</h3>', '<h3><i class=\'bx bx-cloud\'></i> <span data-i18n="settings_cloud_sync">المزامنة السحابية</span></h3>'),
    ("<i class='bx bx-cloud-upload'></i> رفع البيانات</button>", "<i class='bx bx-cloud-upload'></i> <span data-i18n=\"btn_push_data\">رفع البيانات</span></button>"),
    ("<i class='bx bx-cloud-download'></i> سحب البيانات</button>", "<i class='bx bx-cloud-download'></i> <span data-i18n=\"btn_pull_data\">سحب البيانات</span></button>"),
    
    # Backup
    ('<h3><i class=\'bx bx-data\'></i> النسخ الاحتياطي</h3>', '<h3><i class=\'bx bx-data\'></i> <span data-i18n="settings_backup">النسخ الاحتياطي</span></h3>'),
    ('<h3><i class=\'bx bx-download\'></i> النسخ الاحتياطي</h3>', '<h3><i class=\'bx bx-download\'></i> <span data-i18n="settings_backup">النسخ الاحتياطي</span></h3>'),
    ("<i class='bx bx-export'></i> تصدير نسخة احتياطية</button>", "<i class='bx bx-export'></i> <span data-i18n=\"btn_export_backup\">تصدير نسخة احتياطية</span></button>"),
    ("<i class='bx bx-import'></i> استيراد نسخة احتياطية</button>", "<i class='bx bx-import'></i> <span data-i18n=\"btn_import_backup\">استيراد نسخة احتياطية</span></button>"),
    
    # Users section
    ('<h3 style="margin:0"><i class=\'bx bx-group\'></i> فريق العمل</h3>', '<h3 style="margin:0"><i class=\'bx bx-group\'></i> <span data-i18n="settings_team">فريق العمل</span></h3>'),
    ('<h3 style="margin:0"><i class=\'bx bx-hard-hat\'></i> المهندسين والفنيين</h3>', '<h3 style="margin:0"><i class=\'bx bx-hard-hat\'></i> <span data-i18n="settings_engineers">المهندسين والفنيين</span></h3>'),
    ('<h3><i class=\'bx bx-history\'></i> سجل النشاط</h3>', '<h3><i class=\'bx bx-history\'></i> <span data-i18n="settings_activity">سجل النشاط</span></h3>'),
    ("<i class='bx bx-refresh'></i> تحديث</button>", "<i class='bx bx-refresh'></i> <span data-i18n=\"btn_refresh\">تحديث</span></button>"),
]

for old, new in replacements:
    content = content.replace(old, new, 1)

# 5. Now inject the translation infrastructure as a <script> block right before the first DB script
translation_script = """<script>
// ========== i18n Translation System ==========
const TRANSLATIONS = {
  ar: {
    // Navigation
    nav_dashboard: 'لوحة التحكم', nav_inventory: 'المخزون', nav_sales: 'البيع',
    nav_purchases: 'المشتريات', nav_maintenance: 'ورشة الصيانة', nav_accounting: 'المحاسبة',
    nav_reports: 'التقارير', nav_settings: 'الإعدادات', nav_products: 'المنتجات',
    nav_categories: 'التصنيفات', nav_import_export: 'استيراد / تصدير',
    nav_invoices: 'الفواتير', nav_clients: 'العملاء', nav_suppliers: 'الموردين',
    nav_summary: 'الملخص', nav_expenses: 'المصروفات',
    nav_daily: 'يومي', nav_monthly: 'شهري', nav_inventory_report: 'المخزون', nav_outstanding: 'المستحقات',
    nav_main: 'الرئيسية', nav_company: 'بيانات الشركة', nav_notifications: 'الإشعارات',
    nav_cloud_sync: 'المزامنة السحابية', nav_backup: 'النسخ الاحتياطي',
    nav_team: 'فريق العمل', nav_activity: 'سجل النشاط',
    nav_home: 'الرئيسية', nav_maintenance_short: 'الصيانة', nav_more: 'المزيد',
    
    // Stats
    stat_sales_today: 'مبيعات اليوم', stat_purchases_today: 'مشتريات اليوم',
    stat_net_profit: 'صافي الربح', stat_under_maintenance: 'أجهزة تحت الصيانة',
    stat_total_products: 'إجمالي المنتجات', stat_total_clients: 'إجمالي العملاء',
    stat_total_suppliers: 'إجمالي الموردين', stat_active_devices: 'أجهزة نشطة',
    stat_under_repair: 'تحت الصيانة', stat_done_not_delivered: 'خلصت ومتسلمتش',
    stat_delivered_not_paid: 'اتسلمت ومدفعتش', stat_completed: 'مكتملة',
    stat_total_revenue: 'إجمالي الإيرادات', stat_total_expenses: 'إجمالي المصروفات',
    stat_owed_by_clients: 'مبالغ مستحقة من العملاء',
    stat_treasury_total: 'إجمالي مصروفات الخزينة',
    stat_indirect_total: 'إجمالي المصروفات غير المباشرة',
    
    // Dashboard
    sales_overview: 'نظرة عامة على المبيعات',
    label_sales: 'المبيعات', label_purchases: 'المشتريات',
    period_week: 'أسبوع', period_month: 'شهر', period_year: 'سنة',
    maint_status: 'حالة الصيانة', top_5_products: 'أكثر 5 منتجات مبيعاً',
    revenue_6_months: 'إيرادات آخر 6 شهور',
    alerts: 'تنبيهات', no_alerts: 'لا توجد تنبيهات',
    recent_invoices: 'آخر الفواتير', no_invoices: 'لا توجد فواتير',
    recent_activity: 'آخر الحركات', no_activity: 'لا توجد حركات',
    tab_operations: 'العمليات', tab_logins: 'تسجيل الدخول',
    show_all_activity: 'عرض كل الحركات',
    quick_actions: 'إجراءات سريعة', period_details: 'تفاصيل الفترة',
    
    // Buttons & Actions
    add_product: 'إضافة صنف', sale_invoice: 'فاتورة بيع',
    purchase_invoice: 'فاتورة شراء', maint_order: 'إذن صيانة',
    scan_barcode: 'مسح باركود', import_export: 'استيراد/تصدير',
    new_sale_invoice: 'فاتورة بيع جديدة', add_client: 'إضافة عميل',
    new_service: 'زيارة/خدمة جديدة', new_purchase_invoice: 'فاتورة شراء جديدة',
    add_supplier: 'إضافة مورد', new_visit: 'زيارة جديدة',
    add_category: 'إضافة تصنيف', add_user: 'إضافة مستخدم',
    add_engineer: 'إضافة مهندس/فني', add_recipient: 'إضافة مستلم',
    add_expense: 'إضافة مصروف', new_device_intake: 'إذن استلام جهاز',
    btn_save: 'حفظ', btn_cancel: 'إلغاء', btn_delete: 'حذف',
    btn_confirm: 'تأكيد', btn_close: 'إغلاق', btn_back: 'رجوع',
    btn_show: 'عرض', btn_refresh: 'تحديث', btn_test: 'اختبار',
    btn_push_data: 'رفع البيانات', btn_pull_data: 'سحب البيانات',
    btn_export_backup: 'تصدير نسخة احتياطية', btn_import_backup: 'استيراد نسخة احتياطية',
    print_pdf: 'طباعة / PDF', save_invoice: 'حفظ الفاتورة',
    
    // Table Headers
    th_code: 'الكود', th_product: 'الصنف', th_condition: 'الحالة',
    th_type: 'النوع', th_category: 'التصنيف', th_buy_price: 'سعر الشراء',
    th_sell_price: 'سعر البيع', th_quantity: 'الكمية', th_min_stock: 'الحد الأدنى',
    th_actions: 'إجراءات', th_date: 'التاريخ', th_client: 'العميل',
    th_invoice_num: 'رقم الفاتورة', th_items: 'الأصناف', th_total: 'الإجمالي',
    th_status: 'الحالة', th_by: 'بواسطة', th_name: 'الاسم',
    th_phone: 'التليفون', th_factory: 'المصنع', th_activity: 'النشاط',
    th_balance: 'الرصيد', th_company: 'الشركة', th_description: 'الوصف',
    th_location: 'الموقع', th_price: 'السعر', th_order_num: 'رقم الأمر',
    th_device: 'الجهاز', th_engineer: 'المهندس', th_problem: 'المشكلة',
    th_intake_date: 'تاريخ الدخول', th_classification: 'التصنيف',
    th_statement: 'البيان', th_amount: 'المبلغ', th_expense_type: 'النوع',
    th_chat_id: 'Chat ID', th_notifications: 'الإشعارات',
    th_username: 'اسم المستخدم', th_role: 'الدور', th_specialty: 'التخصص',
    th_source: 'المصدر', th_notes: 'ملاحظات', th_num: 'رقم',
    
    // Tabs
    tab_invoices: 'الفواتير', tab_clients: 'العملاء', tab_services: 'خدمات وزيارات',
    tab_suppliers: 'الموردين', tab_devices: 'أجهزة', tab_visits: 'زيارات وخدمات',
    tab_treasury: 'مصروفات خزينة', tab_indirect: 'مصروفات غير مباشرة', tab_all: 'الكل',
    tab_daily: 'يومي', tab_monthly: 'شهري', tab_inventory: 'المخزون', tab_outstanding: 'المستحقات',
    
    // Filters
    filter_all: 'الكل', all_categories: 'كل التصنيفات',
    cond_new: 'جديد', cond_used: 'مستعمل',
    type_device: 'جهاز', type_part: 'قطعة غيار',
    no_category: 'بدون تصنيف',
    
    // Search placeholders
    search_name_code: 'بحث بالاسم أو الكود...',
    search_invoices: 'بحث في الفواتير...',
    search_clients: 'بحث في العملاء...',
    search_services: 'بحث في الخدمات...',
    search_suppliers: 'بحث في الموردين...',
    search_name_order: 'بحث بالاسم أو رقم الأمر...',
    search_visits: 'بحث في الزيارات...',
    search_categories: 'بحث في التصنيفات...',
    
    // Form labels
    label_sku: 'كود الصنف (SKU)', label_product_name: 'اسم الصنف *',
    label_condition: 'الحالة *', label_type: 'النوع *', label_category: 'التصنيف',
    label_buy_price: 'سعر الشراء (ج.م) *', label_sell_price: 'سعر البيع (ج.م) *',
    label_quantity: 'الكمية *', label_min_stock: 'الحد الأدنى للمخزون',
    label_barcode: 'باركود', label_description: 'الوصف', label_image: 'صورة',
    label_company_name: 'اسم الشركة', label_phone: 'التليفون',
    label_address: 'العنوان', label_tax_number: 'الرقم الضريبي',
    label_vat_rate: 'نسبة الضريبة %', label_logo: 'اللوجو',
    label_company: 'الشركة', label_cloud_sync: 'المزامنة السحابية',
    label_team: 'فريق العمل', label_version: 'إصدار النظام',
    
    // Empty states
    no_products: 'لا توجد أصناف بعد', no_clients: 'لا يوجد عملاء',
    no_services: 'لا توجد زيارات أو خدمات', no_purchase_invoices: 'لا توجد فواتير شراء',
    no_suppliers: 'لا يوجد موردين', no_devices: 'لا توجد أجهزة في الصيانة',
    no_visits: 'لا توجد زيارات', no_sale_invoices: 'لا توجد فواتير بيع',
    no_categories: 'لا توجد تصنيفات بعد', no_engineers: 'لا يوجد مهندسين أو فنيين',
    no_recipients: 'لا يوجد مستلمين — أضف Chat ID لبدء الإشعارات',
    low_stock_alert: 'أصناف وصلت للحد الأدنى!',
    
    // Modals
    modal_add_product: 'إضافة صنف جديد', modal_edit_product: 'تعديل صنف',
    modal_manage_categories: 'إدارة التصنيفات', modal_stock_in: 'إضافة للمخزون',
    modal_stock_out: 'صرف من المخزون', modal_import_export: 'استيراد / تصدير المخزون',
    modal_product_details: 'تفاصيل الصنف', modal_add_expense: 'إضافة مصروف',
    modal_add_user: 'إضافة مستخدم', modal_edit_user: 'تعديل مستخدم',
    modal_add_engineer: 'إضافة مهندس/فني', modal_edit_engineer: 'تعديل مهندس/فني',
    modal_new_device: 'إذن استلام جهاز جديد', modal_edit_device: 'تعديل بيانات الجهاز',
    modal_add_client: 'إضافة عميل جديد', modal_edit_client: 'تعديل عميل',
    modal_repair_history: 'تاريخ الصيانة',
    modal_add_supplier: 'إضافة مورد جديد', modal_edit_supplier: 'تعديل مورد',
    modal_new_invoice: 'فاتورة جديدة', modal_add_recipient: 'إضافة مستلم',
    modal_new_service: 'زيارة/خدمة جديدة', modal_payment_ledger: 'سجل المدفوعات',
    modal_client_data: 'بيانات العميل', modal_sale_invoice: 'فاتورة بيع',
    modal_purchase_invoice: 'فاتورة شراء',
    
    // Settings
    settings_company: 'بيانات الشركة', settings_telegram: 'إعدادات Telegram Bot',
    recipients: 'المستلمين', settings_cloud_sync: 'المزامنة السحابية',
    settings_backup: 'النسخ الاحتياطي', settings_team: 'فريق العمل',
    settings_engineers: 'المهندسين والفنيين', settings_activity: 'سجل النشاط',
    expenses: 'المصروفات',
    client_balances: 'أرصدة العملاء (مين عليه فلوس)',
    supplier_balances: 'أرصدة الموردين (مين لينا عنده فلوس)',
    
    // Roles
    role_admin: 'مدير', role_manager: 'مشرف', role_staff: 'موظف',
    
    // Device statuses
    device_under_repair: '🔧 تحت الصيانة',
    device_done_not_delivered: '✅ خلصت ومتسلمتش',
    device_delivered_not_paid: '📦 اتسلمت ومدفعتش',
    device_completed: '💰 خلصت واتدفعت',
    
    // Service statuses
    service_pending: 'قيد الانتظار', service_in_progress: 'جاري التنفيذ',
    service_completed: 'مكتملة', service_cancelled: 'ملغاة',
    
    // Invoice statuses
    invoice_paid: 'مدفوعة', invoice_unpaid: 'غير مدفوعة', invoice_partial: 'دفع جزئي',
    
    // Product badges
    badge_new: 'جديد', badge_used: 'مستعمل',
    badge_device: 'جهاز', badge_part: 'قطعة غيار',
    
    // Page titles
    page_dashboard: 'لوحة التحكم', page_inventory: 'المخزون', page_categories: 'التصنيفات',
    page_sales: 'البيع', page_purchases: 'المشتريات', page_maintenance: 'ورشة الصيانة',
    page_accounting: 'المحاسبة', page_reports: 'التقارير', page_settings: 'الإعدادات',
    
    // Toast messages
    toast_save_error: 'خطأ في حفظ البيانات — حاول مرة أخرى',
    toast_connection_error: 'خطأ في الاتصال بالسيرفر',
    toast_added_to_list: 'تم إضافة للقائمة ✅',
    toast_item_exists: 'العنصر موجود بالفعل',
    toast_list_saved: 'تم حفظ القائمة ✅',
    toast_backup_exported: 'تم تصدير النسخة الاحتياطية',
    toast_imported: 'تم الاستيراد ✅',
    toast_file_error: 'خطأ في الملف',
    toast_scanner_not_supported: 'متصفحك لا يدعم مسح الباركود',
    toast_camera_error: 'فشل الوصول للكاميرا',
    toast_product_added: 'تم إضافة الصنف',
    toast_product_updated: 'تم تعديل الصنف',
    toast_product_deleted: 'تم حذف الصنف',
    toast_product_not_found: 'لم يتم العثور على منتج بهذا الباركود',
    toast_enter_product_name: 'اكتب اسم الصنف',
    toast_enter_quantity: 'أدخل كمية صحيحة',
    toast_product_missing: 'الصنف غير موجود',
    toast_category_exists: 'التصنيف موجود بالفعل',
    toast_category_added: 'تم إضافة التصنيف',
    toast_category_deleted: 'تم حذف التصنيف',
    toast_cant_delete_category_items: 'لا يمكن حذف تصنيف به أصناف',
    toast_cant_delete_category_children: 'لا يمكن حذف تصنيف له تصنيفات فرعية',
    toast_enter_category_name: 'أدخل اسم التصنيف',
    toast_system_load_error: 'خطأ في تحميل النظام — تأكد من الاتصال بالإنترنت',
    toast_code_copied: 'تم نسخ الكود ✅',
    
    // Misc
    logout: 'تسجيل الخروج',
    selected_count: 'محدد',
    delete_selected: 'حذف المحدد',
    not_connected: 'غير متصل',
    connected: 'متصل',
    currency: 'ج.م',
    report_date_label: 'التاريخ:',
    report_month_label: 'الشهر:',
    
    // Invoice summary
    inv_subtotal: 'الإجمالي الفرعي:', inv_total: 'الإجمالي:',
    
    // Repair cost
    repair_stock_cost: 'تكلفة قطع المخزون:', repair_external_cost: 'تكلفة القطع الخارجية:',
    repair_total_cost: 'التكلفة الإجمالية:', repair_profit: 'الربح:',
  },
  en: {
    // Navigation
    nav_dashboard: 'Dashboard', nav_inventory: 'Inventory', nav_sales: 'Sales',
    nav_purchases: 'Purchases', nav_maintenance: 'Workshop', nav_accounting: 'Accounting',
    nav_reports: 'Reports', nav_settings: 'Settings', nav_products: 'Products',
    nav_categories: 'Categories', nav_import_export: 'Import / Export',
    nav_invoices: 'Invoices', nav_clients: 'Clients', nav_suppliers: 'Suppliers',
    nav_summary: 'Summary', nav_expenses: 'Expenses',
    nav_daily: 'Daily', nav_monthly: 'Monthly', nav_inventory_report: 'Inventory', nav_outstanding: 'Outstanding',
    nav_main: 'Main', nav_company: 'Company Info', nav_notifications: 'Notifications',
    nav_cloud_sync: 'Cloud Sync', nav_backup: 'Backup',
    nav_team: 'Team', nav_activity: 'Activity Log',
    nav_home: 'Home', nav_maintenance_short: 'Maintenance', nav_more: 'More',
    
    // Stats
    stat_sales_today: 'Sales Today', stat_purchases_today: 'Purchases Today',
    stat_net_profit: 'Net Profit', stat_under_maintenance: 'Under Maintenance',
    stat_total_products: 'Total Products', stat_total_clients: 'Total Clients',
    stat_total_suppliers: 'Total Suppliers', stat_active_devices: 'Active Devices',
    stat_under_repair: 'Under Repair', stat_done_not_delivered: 'Done, Not Delivered',
    stat_delivered_not_paid: 'Delivered, Not Paid', stat_completed: 'Completed',
    stat_total_revenue: 'Total Revenue', stat_total_expenses: 'Total Expenses',
    stat_owed_by_clients: 'Owed by Clients',
    stat_treasury_total: 'Treasury Expenses Total',
    stat_indirect_total: 'Indirect Expenses Total',
    
    // Dashboard
    sales_overview: 'Sales Overview',
    label_sales: 'Sales', label_purchases: 'Purchases',
    period_week: 'Week', period_month: 'Month', period_year: 'Year',
    maint_status: 'Maintenance Status', top_5_products: 'Top 5 Best Sellers',
    revenue_6_months: 'Revenue Last 6 Months',
    alerts: 'Alerts', no_alerts: 'No alerts',
    recent_invoices: 'Recent Invoices', no_invoices: 'No invoices',
    recent_activity: 'Recent Activity', no_activity: 'No activity',
    tab_operations: 'Operations', tab_logins: 'Logins',
    show_all_activity: 'Show All Activity',
    quick_actions: 'Quick Actions', period_details: 'Period Details',
    
    // Buttons & Actions
    add_product: 'Add Product', sale_invoice: 'Sale Invoice',
    purchase_invoice: 'Purchase Invoice', maint_order: 'Maintenance Order',
    scan_barcode: 'Scan Barcode', import_export: 'Import/Export',
    new_sale_invoice: 'New Sale Invoice', add_client: 'Add Client',
    new_service: 'New Service/Visit', new_purchase_invoice: 'New Purchase Invoice',
    add_supplier: 'Add Supplier', new_visit: 'New Visit',
    add_category: 'Add Category', add_user: 'Add User',
    add_engineer: 'Add Engineer/Tech', add_recipient: 'Add Recipient',
    add_expense: 'Add Expense', new_device_intake: 'New Device Intake',
    btn_save: 'Save', btn_cancel: 'Cancel', btn_delete: 'Delete',
    btn_confirm: 'Confirm', btn_close: 'Close', btn_back: 'Back',
    btn_show: 'Show', btn_refresh: 'Refresh', btn_test: 'Test',
    btn_push_data: 'Push Data', btn_pull_data: 'Pull Data',
    btn_export_backup: 'Export Backup', btn_import_backup: 'Import Backup',
    print_pdf: 'Print / PDF', save_invoice: 'Save Invoice',
    
    // Table Headers
    th_code: 'Code', th_product: 'Product', th_condition: 'Condition',
    th_type: 'Type', th_category: 'Category', th_buy_price: 'Buy Price',
    th_sell_price: 'Sell Price', th_quantity: 'Qty', th_min_stock: 'Min Stock',
    th_actions: 'Actions', th_date: 'Date', th_client: 'Client',
    th_invoice_num: 'Invoice #', th_items: 'Items', th_total: 'Total',
    th_status: 'Status', th_by: 'By', th_name: 'Name',
    th_phone: 'Phone', th_factory: 'Factory', th_activity: 'Activity',
    th_balance: 'Balance', th_company: 'Company', th_description: 'Description',
    th_location: 'Location', th_price: 'Price', th_order_num: 'Order #',
    th_device: 'Device', th_engineer: 'Engineer', th_problem: 'Problem',
    th_intake_date: 'Intake Date', th_classification: 'Classification',
    th_statement: 'Statement', th_amount: 'Amount', th_expense_type: 'Type',
    th_chat_id: 'Chat ID', th_notifications: 'Notifications',
    th_username: 'Username', th_role: 'Role', th_specialty: 'Specialty',
    th_source: 'Source', th_notes: 'Notes', th_num: '#',
    
    // Tabs
    tab_invoices: 'Invoices', tab_clients: 'Clients', tab_services: 'Services & Visits',
    tab_suppliers: 'Suppliers', tab_devices: 'Devices', tab_visits: 'Visits & Services',
    tab_treasury: 'Treasury Expenses', tab_indirect: 'Indirect Expenses', tab_all: 'All',
    tab_daily: 'Daily', tab_monthly: 'Monthly', tab_inventory: 'Inventory', tab_outstanding: 'Outstanding',
    
    // Filters
    filter_all: 'All', all_categories: 'All Categories',
    cond_new: 'New', cond_used: 'Used',
    type_device: 'Device', type_part: 'Spare Part',
    no_category: 'No Category',
    
    // Search placeholders
    search_name_code: 'Search by name or code...',
    search_invoices: 'Search invoices...',
    search_clients: 'Search clients...',
    search_services: 'Search services...',
    search_suppliers: 'Search suppliers...',
    search_name_order: 'Search by name or order #...',
    search_visits: 'Search visits...',
    search_categories: 'Search categories...',
    
    // Form labels
    label_sku: 'SKU Code', label_product_name: 'Product Name *',
    label_condition: 'Condition *', label_type: 'Type *', label_category: 'Category',
    label_buy_price: 'Buy Price (EGP) *', label_sell_price: 'Sell Price (EGP) *',
    label_quantity: 'Quantity *', label_min_stock: 'Min Stock Level',
    label_barcode: 'Barcode', label_description: 'Description', label_image: 'Image',
    label_company_name: 'Company Name', label_phone: 'Phone',
    label_address: 'Address', label_tax_number: 'Tax Number',
    label_vat_rate: 'VAT Rate %', label_logo: 'Logo',
    label_company: 'Company', label_cloud_sync: 'Cloud Sync',
    label_team: 'Team', label_version: 'System Version',
    
    // Empty states
    no_products: 'No products yet', no_clients: 'No clients',
    no_services: 'No services or visits', no_purchase_invoices: 'No purchase invoices',
    no_suppliers: 'No suppliers', no_devices: 'No devices in maintenance',
    no_visits: 'No visits', no_sale_invoices: 'No sale invoices',
    no_categories: 'No categories yet', no_engineers: 'No engineers or technicians',
    no_recipients: 'No recipients — Add a Chat ID to start notifications',
    low_stock_alert: 'items reached minimum stock!',
    
    // Modals
    modal_add_product: 'Add New Product', modal_edit_product: 'Edit Product',
    modal_manage_categories: 'Manage Categories', modal_stock_in: 'Stock In',
    modal_stock_out: 'Stock Out', modal_import_export: 'Import / Export Inventory',
    modal_product_details: 'Product Details', modal_add_expense: 'Add Expense',
    modal_add_user: 'Add User', modal_edit_user: 'Edit User',
    modal_add_engineer: 'Add Engineer/Tech', modal_edit_engineer: 'Edit Engineer/Tech',
    modal_new_device: 'New Device Intake', modal_edit_device: 'Edit Device',
    modal_add_client: 'Add New Client', modal_edit_client: 'Edit Client',
    modal_repair_history: 'Repair History',
    modal_add_supplier: 'Add New Supplier', modal_edit_supplier: 'Edit Supplier',
    modal_new_invoice: 'New Invoice', modal_add_recipient: 'Add Recipient',
    modal_new_service: 'New Service/Visit', modal_payment_ledger: 'Payment Ledger',
    modal_client_data: 'Client Details', modal_sale_invoice: 'Sale Invoice',
    modal_purchase_invoice: 'Purchase Invoice',
    
    // Settings
    settings_company: 'Company Info', settings_telegram: 'Telegram Bot Settings',
    recipients: 'Recipients', settings_cloud_sync: 'Cloud Sync',
    settings_backup: 'Backup', settings_team: 'Team',
    settings_engineers: 'Engineers & Technicians', settings_activity: 'Activity Log',
    expenses: 'Expenses',
    client_balances: 'Client Balances (Who Owes You)',
    supplier_balances: 'Supplier Balances (Who You Owe)',
    
    // Roles
    role_admin: 'Admin', role_manager: 'Manager', role_staff: 'Staff',
    
    // Device statuses
    device_under_repair: '🔧 Under Repair',
    device_done_not_delivered: '✅ Done, Not Delivered',
    device_delivered_not_paid: '📦 Delivered, Not Paid',
    device_completed: '💰 Completed & Paid',
    
    // Service statuses
    service_pending: 'Pending', service_in_progress: 'In Progress',
    service_completed: 'Completed', service_cancelled: 'Cancelled',
    
    // Invoice statuses
    invoice_paid: 'Paid', invoice_unpaid: 'Unpaid', invoice_partial: 'Partial',
    
    // Product badges
    badge_new: 'New', badge_used: 'Used',
    badge_device: 'Device', badge_part: 'Spare Part',
    
    // Page titles
    page_dashboard: 'Dashboard', page_inventory: 'Inventory', page_categories: 'Categories',
    page_sales: 'Sales', page_purchases: 'Purchases', page_maintenance: 'Workshop',
    page_accounting: 'Accounting', page_reports: 'Reports', page_settings: 'Settings',
    
    // Toast messages
    toast_save_error: 'Error saving data — please try again',
    toast_connection_error: 'Server connection error',
    toast_added_to_list: 'Added to list ✅',
    toast_item_exists: 'Item already exists',
    toast_list_saved: 'List saved ✅',
    toast_backup_exported: 'Backup exported',
    toast_imported: 'Imported ✅',
    toast_file_error: 'File error',
    toast_scanner_not_supported: 'Your browser doesn\\'t support barcode scanning',
    toast_camera_error: 'Camera access failed',
    toast_product_added: 'Product added',
    toast_product_updated: 'Product updated',
    toast_product_deleted: 'Product deleted',
    toast_product_not_found: 'No product found with this barcode',
    toast_enter_product_name: 'Enter product name',
    toast_enter_quantity: 'Enter a valid quantity',
    toast_product_missing: 'Product not found',
    toast_category_exists: 'Category already exists',
    toast_category_added: 'Category added',
    toast_category_deleted: 'Category deleted',
    toast_cant_delete_category_items: 'Cannot delete category with products',
    toast_cant_delete_category_children: 'Cannot delete category with subcategories',
    toast_enter_category_name: 'Enter category name',
    toast_system_load_error: 'System loading error — check your internet connection',
    toast_code_copied: 'Code copied ✅',
    
    // Misc
    logout: 'Logout',
    selected_count: 'selected',
    delete_selected: 'Delete Selected',
    not_connected: 'Not Connected',
    connected: 'Connected',
    currency: 'EGP',
    report_date_label: 'Date:',
    report_month_label: 'Month:',
    
    // Invoice summary
    inv_subtotal: 'Subtotal:', inv_total: 'Total:',
    
    // Repair cost
    repair_stock_cost: 'Stock Parts Cost:', repair_external_cost: 'External Parts Cost:',
    repair_total_cost: 'Total Cost:', repair_profit: 'Profit:',
  }
};

let currentLang = localStorage.getItem('sms-lang') || 'ar';

function t(key) {
  return (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) || (TRANSLATIONS.ar[key]) || key;
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('sms-lang', lang);
  document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
  document.documentElement.lang = lang;
  
  // Update all data-i18n elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
      el.textContent = TRANSLATIONS[lang][key];
    }
  });
  
  // Update all data-i18n-placeholder elements
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
      el.placeholder = TRANSLATIONS[lang][key];
    }
  });
  
  // Update language toggle button
  const toggleBtn = document.getElementById('lang-toggle');
  if (toggleBtn) toggleBtn.textContent = lang === 'ar' ? 'EN' : 'عربي';
  
  // Update PAGE_TITLES if available
  if (typeof PAGE_TITLES !== 'undefined') {
    PAGE_TITLES.dashboard = t('page_dashboard');
    PAGE_TITLES.inventory = t('page_inventory');
    PAGE_TITLES.categories = t('page_categories');
    PAGE_TITLES.sales = t('page_sales');
    PAGE_TITLES.purchases = t('page_purchases');
    PAGE_TITLES.maintenance = t('page_maintenance');
    PAGE_TITLES.accounting = t('page_accounting');
    PAGE_TITLES.reports = t('page_reports');
    PAGE_TITLES.settings = t('page_settings');
  }
  
  // Update current page title
  const pageTitleEl = document.getElementById('page-title');
  if (pageTitleEl && typeof PAGE_TITLES !== 'undefined') {
    const currentPage = document.querySelector('.page.active')?.id?.replace('page-', '');
    if (currentPage && PAGE_TITLES[currentPage]) {
      pageTitleEl.textContent = PAGE_TITLES[currentPage];
    }
  }
  
  // Update DEVICE_STATUSES labels if available
  if (typeof DEVICE_STATUSES !== 'undefined') {
    DEVICE_STATUSES.under_repair.label = t('device_under_repair');
    DEVICE_STATUSES.done_not_delivered.label = t('device_done_not_delivered');
    DEVICE_STATUSES.delivered_not_paid.label = t('device_delivered_not_paid');
    DEVICE_STATUSES.completed.label = t('device_completed');
  }
}

function toggleLanguage() {
  setLanguage(currentLang === 'ar' ? 'en' : 'ar');
}

// Apply language on load
document.addEventListener('DOMContentLoaded', function() {
  // Small delay to ensure all scripts are loaded
  setTimeout(() => setLanguage(currentLang), 100);
});
</script>
"""

# Insert the translation script right before the DB script
content = content.replace(
    "<script>/**\n * SMS System — IndexedDB Database Layer\n */",
    translation_script + "\n<script>/**\n * SMS System — IndexedDB Database Layer\n */"
)

# 6. Update some key JS functions to use t() for dynamic content

# Update renderProducts condition badges
content = content.replace(
    "const condBadge = p.condition === 'new' \n      ? '<span class=\"badge badge-new\">جديد</span>' \n      : '<span class=\"badge badge-used\">مستعمل</span>';",
    "const condBadge = p.condition === 'new' \n      ? '<span class=\"badge badge-new\">' + t('badge_new') + '</span>' \n      : '<span class=\"badge badge-used\">' + t('badge_used') + '</span>';"
)
content = content.replace(
    "const typeBadge = p.type === 'device'\n      ? '<span class=\"badge badge-device\">جهاز</span>'\n      : '<span class=\"badge badge-part\">قطعة غيار</span>';",
    "const typeBadge = p.type === 'device'\n      ? '<span class=\"badge badge-device\">' + t('badge_device') + '</span>'\n      : '<span class=\"badge badge-part\">' + t('badge_part') + '</span>';"
)

# Update grid empty state
content = content.replace(
    "grid.innerHTML = '<div class=\"empty-state\" style=\"grid-column:1/-1\"><i class=\"bx bx-package\" style=\"font-size:48px;color:#ccc\"></i><p>لا توجد أصناف</p></div>';",
    "grid.innerHTML = '<div class=\"empty-state\" style=\"grid-column:1/-1\"><i class=\"bx bx-package\" style=\"font-size:48px;color:#ccc\"></i><p>' + t('no_products') + '</p></div>';"
)

# Update view-product modal title override
content = content.replace(
    "document.querySelector('#modal-view-product .modal-header h3').textContent = 'بيانات العميل';",
    "document.querySelector('#modal-view-product .modal-header h3').textContent = t('modal_client_data');"
)
content = content.replace(
    "document.querySelector('#modal-view-product .modal-header h3').textContent = isSale ? 'فاتورة بيع' : 'فاتورة شراء';",
    "document.querySelector('#modal-view-product .modal-header h3').textContent = isSale ? t('modal_sale_invoice') : t('modal_purchase_invoice');"
)

# Write the result
with open('/tmp/sms-system/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Transformations applied successfully.")
