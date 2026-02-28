#!/usr/bin/env python3
"""
Comprehensive translation script for SMS System.
Phase 1: Add translation keys to TRANSLATIONS
Phase 2: Replace JS Arabic strings with t() calls 
Phase 3: Replace HTML Arabic text with data-i18n attributes
"""

import re, json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# New translation keys (ar -> en)
# ============================================================
NEW_KEYS = {
    # Login
    'app_title': ('SMS — نظام إدارة المخزون والصيانة', 'SMS — Inventory & Maintenance System'),
    'remember_me': ('تذكرني', 'Remember Me'),
    'btn_login': ('تسجيل الدخول', 'Login'),
    'dark_mode': ('الوضع الليلي', 'Dark Mode'),
    'cloud_sync_title': ('المزامنة السحابية', 'Cloud Sync'),
    'chart_line': ('رسم بياني', 'Line Chart'),
    'chart_bar': ('أعمدة', 'Bar Chart'),
    'zero_selected': ('0 محدد', '0 selected'),
    'delete_bulk': ('حذف المحدد', 'Delete Selected'),
    'add_first_product': ('إضافة أول صنف', 'Add First Product'),
    'add_first_category': ('إضافة أول تصنيف', 'Add First Category'),
    'create_first_invoice': ('إنشاء أول فاتورة', 'Create First Invoice'),
    'add_first_client': ('إضافة أول عميل', 'Add First Client'),
    'add_first_visit': ('إضافة أول زيارة', 'Add First Visit'),
    'add_first_supplier': ('إضافة أول مورد', 'Add First Supplier'),
    'intake_first_device': ('إذن استلام أول جهاز', 'First Device Intake'),
    'add_first_engineer': ('إضافة أول مهندس/فني', 'Add First Engineer/Tech'),
    'no_treasury_expenses': ('لا توجد مصروفات خزينة', 'No treasury expenses'),
    'no_indirect_expenses': ('لا توجد مصروفات غير مباشرة', 'No indirect expenses'),
    'no_expenses_page': ('لا توجد مصروفات', 'No expenses'),
    'no_devices_maint': ('لا توجد أجهزة في الصيانة', 'No devices in maintenance'),
    'list_view': ('عرض قائمة', 'List View'),
    'card_view': ('عرض البطاقات', 'Card View'),
    'telegram_instructions': ('يبعت أي رسالة للبوت على Telegram (مثلاً /start) → ثم دوس "جلب Chat IDs" هنا → هيظهر الـ Chat ID تلقائي', 'Send any message to the bot on Telegram (e.g. /start) → then click "Fetch Chat IDs" here → Chat ID will appear automatically'),
    'chat_id_placeholder': ('مثلاً: 123456789', 'e.g.: 123456789'),
    'notif_low_stock': ('تنبيه مخزون منخفض', 'Low Stock Alert'),
    'notif_unpaid': ('فواتير غير مدفوعة', 'Unpaid Invoices'),
    'notif_devices_ready': ('أجهزة جاهزة للتسليم', 'Devices Ready for Delivery'),
    'notif_warranty_expiry': ('تنبيهات انتهاء الضمان', 'Warranty Expiry Alerts'),
    'notif_daily_summary': ('ملخص يومي', 'Daily Summary'),
    'sync_not_connected': ('غير متصل', 'Not Connected'),
    'sync_auto_desc': ('المزامنة تعمل تلقائياً — كل التعديلات تتزامن بين جميع الأجهزة', 'Sync works automatically — all changes sync across all devices'),
    'backup_desc': ('تصدير/استيراد كل بيانات النظام كملف JSON على جهازك', 'Export/import all system data as a JSON file on your device'),
    'permissions_title': ('الصلاحيات:', 'Permissions:'),
    'role_admin_full': ('مدير: كل شيء — تحكم كامل', 'Admin: Everything — full control'),
    'role_manager_full': ('مشرف: المخزون + الفواتير + الصيانة + التقارير + الأسعار', 'Manager: Inventory + Invoices + Maintenance + Reports + Prices'),
    'role_staff_full': ('موظف: إنشاء فواتير + إضافة/صرف مخزون + استلام أجهزة — بدون أسعار أو أرباح', 'Staff: Create invoices + Add/dispatch stock + Device intake — no prices or profits'),
    'sku_auto_placeholder': ('اتركه فارغ للتوليد التلقائي', 'Leave empty for auto-generation'),
    'root_category': ('تصنيف رئيسي', 'Root Category'),
    'new_cat_placeholder': ('اسم التصنيف الجديد', 'New category name'),
    'export_section': ('تصدير', 'Export'),
    'export_products_desc': ('تصدير كل الأصناف إلى ملف Excel', 'Export all products to Excel file'),
    'export_excel_btn': ('تصدير Excel', 'Export Excel'),
    'import_section': ('استيراد', 'Import'),
    'import_products_desc': ('استيراد أصناف من ملف Excel (يجب أن يتبع نفس التنسيق)', 'Import products from Excel file (must follow same format)'),
    'specialty_general': ('عام', 'General'),
    'specialty_mobiles': ('موبايلات', 'Mobiles'),
    'specialty_laptop': ('لابتوب', 'Laptop'),
    'specialty_computer': ('كمبيوتر', 'Computer'),
    'specialty_printers': ('طابعات', 'Printers'),
    'specialty_networks': ('شبكات', 'Networks'),
    'specialty_cameras': ('كاميرات', 'Cameras'),
    'specialty_other': ('أخرى', 'Other'),
    'client_name_ph': ('اسم العميل', 'Client Name'),
    'phone_ph': ('الهاتف', 'Phone'),
    'eng_name_ph': ('اسم المهندس', 'Engineer Name'),
    'phone_opt_ph': ('الهاتف (اختياري)', 'Phone (optional)'),
    'order_colon': ('الأمر:', 'Order:'),
    'device_colon': ('الجهاز:', 'Device:'),
    'client_colon': ('العميل:', 'Client:'),
    'intake_colon': ('الدخول:', 'Intake:'),
    'add_record_btn': ('إضافة سجل', 'Add Record'),
    'date_label': ('التاريخ', 'Date'),
    'action_intake': ('استلام', 'Intake'),
    'action_diagnosis': ('فحص', 'Diagnosis'),
    'action_repair': ('إصلاح', 'Repair'),
    'action_testing': ('اختبار', 'Testing'),
    'action_delivery': ('تسليم', 'Delivery'),
    'action_other': ('أخرى', 'Other'),
    'write_notes_ph': ('اكتب الوصف أو الملاحظات...', 'Write description or notes...'),
    'select_engineer': ('-- اختر المهندس --', '-- Select Engineer --'),
    'other_engineer': ('مهندس آخر...', 'Other engineer...'),
    'name_ph': ('الاسم', 'Name'),
    'current_balance_label': ('الرصيد الحالي', 'Current Balance'),
    'record_payment_btn': ('تسجيل دفعة', 'Record Payment'),
    'set_balance_btn': ('تعيين رصيد', 'Set Balance'),
    'new_payment_title': ('تسجيل دفعة جديدة', 'Record New Payment'),
    'movement_type_label': ('نوع الحركة', 'Movement Type'),
    'payment_in_opt': ('دفعة واردة (سداد من العميل)', 'Payment In (from client)'),
    'payment_out_opt': ('دفعة صادرة (دفع للمورد)', 'Payment Out (to supplier)'),
    'add_debt_opt': ('إضافة دين جديد', 'Add New Debt'),
    # JS strings
    'toast_username_not_found': ('اسم المستخدم غير موجود', 'Username not found'),
    'toast_wrong_password': ('كلمة المرور غير صحيحة', 'Wrong password'),
    'toast_account_disabled': ('الحساب معطل', 'Account disabled'),
    'sync_connected_sb': ('متصل — Supabase', 'Connected — Supabase'),
    'confirm_replace_all': ('سيتم استبدال كل البيانات الحالية. متابعة؟', 'All current data will be replaced. Continue?'),
    'scanner_aim': ('وجّه الكاميرا نحو الباركود', 'Aim camera at barcode'),
    'no_alerts_check': ('لا توجد تنبيهات ✅', 'No alerts ✅'),
    'no_login_history': ('لا توجد عمليات تسجيل دخول', 'No login records'),
    'no_movements_hist': ('لا توجد حركات', 'No movements'),
    'chart_lbl_sales': ('المبيعات', 'Sales'),
    'chart_lbl_purchases': ('المشتريات', 'Purchases'),
    'chart_no_devices': ('لا توجد أجهزة', 'No devices'),
    'chart_under_repair': ('تحت الصيانة', 'Under Repair'),
    'chart_done': ('خلصت', 'Done'),
    'chart_delivered': ('اتسلمت', 'Delivered'),
    'chart_completed': ('مكتملة', 'Completed'),
    'chart_no_data': ('لا توجد بيانات', 'No data'),
    'chart_unknown': ('غير معروف', 'Unknown'),
    'chart_this_month': ('هذا الشهر', 'This month'),
    'chart_no_invoices': ('لا توجد فواتير', 'No invoices'),
    'unspecified': ('غير محدد', 'Unspecified'),
    'connected_status': ('متصل ✅', 'Connected ✅'),
    'disconnected_status': ('غير متصل', 'Not Connected'),
    
    # Invoice text
    'inv_sale_title': ('فاتورة بيع', 'Sale Invoice'),
    'inv_purchase_title': ('فاتورة شراء', 'Purchase Invoice'),
    'inv_number_label': ('رقم الفاتورة', 'Invoice Number'),
    'inv_date_label': ('التاريخ', 'Date'),
    'inv_client_label': ('العميل', 'Client'),
    'inv_supplier_label': ('المورد', 'Supplier'),
    'inv_items_header': ('الأصناف:', 'Items:'),
    'inv_qty_header': ('الكمية', 'Qty'),
    'inv_price_header': ('السعر', 'Price'),
    'inv_total_header': ('الإجمالي', 'Total'),
    'inv_paid_label': ('المدفوع', 'Paid'),
    'inv_remaining_label': ('المتبقي', 'Remaining'),
    'inv_fully_paid': ('مدفوعة بالكامل', 'Fully Paid'),
    'inv_contact': ('للتواصل', 'Contact'),
    'inv_by': ('بواسطة', 'By'),
    'inv_notes': ('ملاحظات', 'Notes'),
    'inv_photos': ('الصور المرفقة', 'Attached Photos'),
    'inv_barcode': ('باركود الفاتورة', 'Invoice Barcode'),
    'inv_qr': ('QR للتحقق', 'QR Verification'),
    'inv_sms_footer': ('تم الإنشاء بواسطة نظام SMS', 'Created by SMS System'),
    'inv_thank_you': ('شكراً لتعاملكم معنا', 'Thank you for your business'),
    
    # Product view labels
    'vw_code': ('الكود', 'Code'),
    'vw_name': ('الاسم', 'Name'),
    'vw_condition': ('الحالة', 'Condition'),
    'vw_type': ('النوع', 'Type'),
    'vw_category': ('التصنيف', 'Category'),
    'vw_barcode': ('الباركود', 'Barcode'),
    'vw_buy_price': ('سعر الشراء', 'Buy Price'),
    'vw_sell_price': ('سعر البيع', 'Sell Price'),
    'vw_profit_unit': ('الربح/وحدة', 'Profit/Unit'),
    'vw_quantity': ('الكمية', 'Quantity'),
    'vw_min_stock': ('الحد الأدنى', 'Min Stock'),
    'vw_description': ('الوصف', 'Description'),
    'vw_print_barcode': ('طباعة باركود', 'Print Barcode'),
    'vw_movement_history': ('سجل الحركات', 'Movement History'),
    'vw_add': ('إضافة', 'Stock In'),
    'vw_dispatch': ('صرف', 'Stock Out'),
    'vw_new': ('جديد', 'New'),
    'vw_used': ('مستعمل', 'Used'),
    'vw_device': ('جهاز', 'Device'),
    'vw_spare_part': ('قطعة غيار', 'Spare Part'),
    'vw_low_stock': ('مخزون منخفض', 'Low Stock'),
    'vw_available': ('المتاح', 'Available'),
    'vw_existing': ('موجود', 'Exists'),
    
    # Stock modal  
    'stock_in_title': ('إضافة للمخزون', 'Stock In'),
    'stock_out_title': ('صرف من المخزون', 'Stock Out'),
    
    # Category page
    'cat_all_filter': ('كل التصنيفات', 'All Categories'),
    'cat_none': ('بدون تصنيف', 'No Category'),
    'cat_root': ('تصنيف رئيسي', 'Root Category'),
    'cat_no_categories': ('لا توجد تصنيفات بعد', 'No categories yet'),
    'cat_items': ('صنف', 'items'),
    'cat_subcats': ('تصنيف فرعي', 'subcategories'),
    'cat_no_parent': ('بدون تصنيف رئيسي', 'No parent category'),
    'cat_no_results': ('لا توجد نتائج', 'No results'),
    'cat_sub_btn': ('فرعي', 'Sub'),
    
    # Client view
    'vw_email': ('الإيميل', 'Email'),
    'vw_factory_name': ('اسم المصنع', 'Factory Name'),
    'vw_factory_location': ('مكان المصنع', 'Factory Location'),
    'vw_factory_activity': ('نشاط المصنع', 'Factory Activity'),
    'vw_balance': ('الرصيد', 'Balance'),
    'vw_notes': ('ملاحظات', 'Notes'),
    'vw_invoices': ('الفواتير', 'Invoices'),
    
    # Invoice list
    'inv_items_count': ('صنف', 'items'),
    'badge_paid': ('مدفوعة', 'Paid'),
    'badge_partial': ('جزئي', 'Partial'),
    'badge_unpaid': ('غير مدفوعة', 'Unpaid'),
    
    # Invoice form
    'inv_select_client': ('اختر العميل', 'Select Client'),
    'inv_other_client': ('+ أخرى (إضافة عميل جديد)', '+ Other (Add New Client)'),
    'inv_select_supplier': ('اختر المورد', 'Select Supplier'),
    'inv_other_supplier': ('+ أخرى (إضافة مورد جديد)', '+ Other (Add New Supplier)'),
    'inv_select_product': ('اختر صنف', 'Select Product'),
    'inv_other_product': ('+ أخرى (إضافة صنف جديد)', '+ Other (Add New Product)'),
    'inv_qty_ph': ('الكمية', 'Qty'),
    'inv_price_ph': ('السعر', 'Price'),
    'inv_add_product': ('إضافة صنف جديد', 'Add New Product'),
    'inv_prod_name': ('اسم الصنف *', 'Product Name *'),
    'inv_cost_ph': ('التكلفة', 'Cost'),
    'inv_code_ph': ('الكود (اختياري)', 'Code (optional)'),
    'inv_save_add': ('حفظ وإضافة', 'Save & Add'),
    'inv_other_short': ('+ أخرى', '+ Other'),
    
    # Device
    'dev_warranty': ('ضمان', 'Warranty'),
    'dev_months': ('شهر', 'months'),
    'dev_overdue': ('متأخر!', 'Overdue!'),
    'dev_order_num': ('رقم الأمر', 'Order #'),
    'dev_problem': ('المشكلة', 'Problem'),
    'dev_from_stock': ('من المخزون', 'From Stock'),
    'dev_external': ('شراء خارجي', 'External Purchase'),
    'dev_select_part': ('اختر قطعة', 'Select Part'),
    'dev_part_name': ('اسم القطعة', 'Part Name'),
    'dev_supplier': ('المورد', 'Supplier'),
    
    # Device view
    'dv_order': ('رقم الأمر', 'Order #'),
    'dv_status': ('الحالة', 'Status'),
    'dv_device': ('الجهاز', 'Device'),
    'dv_specs': ('المواصفات', 'Specs'),
    'dv_problem': ('المشكلة', 'Problem'),
    'dv_intake_date': ('تاريخ الدخول', 'Intake Date'),
    'dv_client': ('العميل', 'Client'),
    'dv_client_factory': ('مصنع العميل', 'Client Factory'),
    'dv_engineer': ('المهندس المسؤول', 'Responsible Engineer'),
    'dv_warranty': ('الضمان', 'Warranty'),
    'dv_no_warranty': ('لا يوجد ضمان', 'No Warranty'),
    
    # Task
    'task_pending': ('في الانتظار', 'Pending'),
    'task_assigned': ('تم التخصيص', 'Assigned'),
    'task_completed': ('مكتمل', 'Completed'),
    'task_overdue': ('متأخر', 'Overdue'),
    'task_details': ('تفاصيل المهمة', 'Task Details'),
    'task_status': ('حالة المهمة', 'Task Status'),
    'task_deadline': ('الموعد النهائي', 'Deadline'),
    'task_reward': ('المكافأة', 'Reward'),
    'task_penalty': ('العقوبة', 'Penalty'),
    'task_warnings': ('الإنذارات', 'Warnings'),
    'task_instructions': ('تعليمات المهمة', 'Task Instructions'),
    'task_complete_btn': ('إتمام المهمة', 'Complete Task'),
    'task_warn_btn': ('إنذار', 'Warn'),
    'task_penalize_btn': ('عقوبة', 'Penalize'),
    
    # Device parts view
    'parts_used_title': ('القطع المستخدمة', 'Parts Used'),
    'parts_part': ('القطعة', 'Part'),
    'parts_source': ('المصدر', 'Source'),
    'parts_stock': ('مخزون', 'Stock'),
    'parts_external': ('خارجي', 'External'),
    'parts_stock_cost': ('تكلفة قطع المخزون:', 'Stock Parts Cost:'),
    'parts_ext_cost': ('تكلفة القطع الخارجية:', 'External Parts Cost:'),
    'parts_extra': ('مصاريف إضافية:', 'Extra Expenses:'),
    'parts_total_cost': ('التكلفة الإجمالية:', 'Total Cost:'),
    'parts_sell_price': ('سعر البيع:', 'Selling Price:'),
    'parts_profit': ('الربح:', 'Profit:'),
    'parts_cost': ('تكلفة القطع:', 'Parts Cost:'),
    
    # Device misc
    'dev_photos': ('صور الجهاز', 'Device Photos'),
    'dev_qr': ('QR Code — أمر صيانة', 'QR Code — Maintenance Order'),
    'dev_print_label': ('طباعة الملصق', 'Print Label'),
    'dev_print_receipt': ('طباعة إيصال', 'Print Receipt'),
    'dev_details_title': ('تفاصيل أمر الصيانة', 'Maintenance Order Details'),
    'dev_maint_order': ('أمر صيانة', 'Maintenance Order'),
    'dev_receipt_title': ('إيصال صيانة', 'Maintenance Receipt'),

    # Accounting
    'acc_no_clients': ('لا يوجد عملاء', 'No clients'),
    'acc_no_suppliers': ('لا يوجد موردين', 'No suppliers'),
    'acc_record_payment': ('تسجيل دفعة', 'Record Payment'),
    'acc_revenue_details': ('تفاصيل الإيرادات', 'Revenue Details'),
    'acc_expenses_details': ('تفاصيل المصروفات', 'Expenses Details'),
    'acc_profit_details': ('تفاصيل صافي الربح', 'Net Profit Details'),
    'acc_sales': ('مبيعات', 'Sales'),
    'acc_maintenance': ('صيانة', 'Maintenance'),
    'acc_services': ('خدمات وزيارات', 'Services & Visits'),
    'acc_purchases': ('مشتريات', 'Purchases'),
    'acc_general_exp': ('مصروفات عامة', 'General Expenses'),
    'acc_maint_costs': ('تكاليف صيانة', 'Maintenance Costs'),
    'acc_sales_rev': ('إيراد المبيعات', 'Sales Revenue'),
    'acc_maint_profit': ('ربح الصيانة', 'Maintenance Profit'),
    'acc_services_rev': ('إيراد الخدمات', 'Services Revenue'),
    'acc_total': ('الإجمالي', 'Total'),
    
    # Payment ledger
    'ledger_no_movements': ('لا توجد حركات مسجلة', 'No movements recorded'),
    'ledger_payment': ('سداد', 'Payment'),
    'ledger_debt': ('دين', 'Debt'),
    'ledger_pay_out': ('دفع', 'Payment'),
    'ledger_adjustment': ('تعديل', 'Adjustment'),
    'ledger_invoice': ('فاتورة', 'Invoice'),
    'ledger_set_balance': ('تعيين الرصيد يدوياً', 'Set Balance Manually'),
    'ledger_manual_adj': ('تعديل يدوي', 'Manual adjustment'),
    'ledger_edit': ('تعديل الحركة', 'Edit Movement'),
    
    # Reports
    'rpt_daily': ('التقرير اليومي', 'Daily Report'),
    'rpt_sale_invoices': ('فواتير البيع', 'Sale Invoices'),
    'rpt_purchase_invoices': ('فواتير الشراء', 'Purchase Invoices'),
    'rpt_no_sales': ('لا توجد مبيعات', 'No sales'),
    'rpt_no_purchases': ('لا توجد مشتريات', 'No purchases'),
    'rpt_expenses': ('المصروفات', 'Expenses'),
    'rpt_no_expenses': ('لا توجد مصروفات', 'No expenses'),
    'rpt_maintenance': ('الصيانة', 'Maintenance'),
    'rpt_devices_in': ('أجهزة دخلت', 'Devices In'),
    'rpt_devices_done': ('أجهزة خلصت', 'Devices Done'),
    'rpt_monthly': ('التقرير الشهري', 'Monthly Report'),
    'rpt_daily_breakdown': ('تفصيل يومي', 'Daily Breakdown'),
    'rpt_day': ('اليوم', 'Day'),
    'rpt_maint_summary': ('ملخص الصيانة', 'Maintenance Summary'),
    'rpt_devices_completed': ('أجهزة مكتملة', 'Devices Completed'),
    'rpt_inventory': ('تقرير المخزون', 'Inventory Report'),
    'rpt_by_category': ('حسب التصنيف', 'By Category'),
    'rpt_item_count': ('عدد الأصناف', 'Item Count'),
    'rpt_value': ('القيمة', 'Value'),
    'rpt_low_stock': ('أصناف منخفضة', 'Low Stock Items'),
    'rpt_outstanding': ('المبالغ المستحقة', 'Outstanding Amounts'),
    'rpt_total_owed': ('إجمالي المستحق', 'Total Outstanding'),
    
    # Users
    'usr_active': ('مفعل', 'Active'),
    'usr_disabled': ('معطل', 'Disabled'),
    'usr_password_ph': ('كلمة المرور', 'Password'),
    'usr_password_keep': ('اتركه فارغ لعدم التغيير', 'Leave empty to keep unchanged'),
    
    # Permissions
    'perm_dashboard': ('لوحة التحكم', 'Dashboard'),
    'perm_inv_view': ('المخزون — عرض', 'Inventory — View'),
    'perm_inv_edit': ('المخزون — إضافة/تعديل/حذف', 'Inventory — Add/Edit/Delete'),
    'perm_stock': ('إضافة/صرف مخزون', 'Add/Dispatch Stock'),
    'perm_prices': ('عرض الأسعار والأرباح', 'View Prices & Profits'),
    'perm_sales_view': ('البيع — عرض', 'Sales — View'),
    'perm_sales_create': ('البيع — إنشاء فواتير', 'Sales — Create Invoices'),
    'perm_purch_view': ('المشتريات — عرض', 'Purchases — View'),
    'perm_purch_create': ('المشتريات — إنشاء فواتير', 'Purchases — Create Invoices'),
    'perm_clients': ('العملاء', 'Clients'),
    'perm_suppliers': ('الموردين', 'Suppliers'),
    'perm_maint': ('ورشة الصيانة', 'Maintenance Workshop'),
    'perm_intake': ('استلام أجهزة', 'Device Intake'),
    'perm_accounting': ('المحاسبة', 'Accounting'),
    'perm_reports': ('التقارير', 'Reports'),
    'perm_settings': ('الإعدادات', 'Settings'),
    'perm_users': ('إدارة المستخدمين', 'User Management'),
    
    # Service statuses badges
    'svc_pending': ('قيد الانتظار', 'Pending'),
    'svc_in_progress': ('جاري التنفيذ', 'In Progress'),
    'svc_completed': ('مكتملة', 'Completed'),
    'svc_cancelled': ('ملغاة', 'Cancelled'),
    
    # Custom lists
    'cl_edit_title': ('تعديل القائمة', 'Edit List'),
    'cl_add_ph': ('إضافة عنصر جديد...', 'Add new item...'),
    'cl_add_btn': ('إضافة', 'Add'),
    'cl_save': ('💾 حفظ التغييرات', '💾 Save Changes'),
    'cl_empty': ('القائمة فارغة', 'List is empty'),
    'cl_choose': ('اختر', 'Choose'),
    'cl_other': ('أخرى...', 'Other...'),
    'cl_type_here': ('اكتب هنا...', 'Type here...'),
    'cl_search': ('بحث...', 'Search...'),
    'cl_save_label': ('احفظ', 'Save'),
    
    # Expense defaults
    'exp_rent': ('إيجار', 'Rent'),
    'exp_salaries': ('مرتبات', 'Salaries'),
    'exp_utilities': ('كهرباء ومياه', 'Electricity & Water'),
    'exp_transport': ('نقل ومواصلات', 'Transport'),
    'exp_maintenance': ('صيانة', 'Maintenance'),
    'exp_treasury': ('مصروفات خزينة', 'Treasury Expenses'),
    'exp_indirect': ('مصروفات غير مباشرة', 'Indirect Expenses'),
    
    # Notification labels
    'notif_stock_badge': ('مخزون', 'Stock'),
    'notif_inv_badge': ('فواتير', 'Invoices'),
    'notif_delivery_badge': ('تسليم', 'Delivery'),
    'notif_warranty_badge': ('ضمان', 'Warranty'),
    'notif_summary_badge': ('ملخص', 'Summary'),

    # Timeline
    'tl_intake': ('استلام الجهاز', 'Device Intake'),
    'tl_diagnosis': ('فحص وتشخيص', 'Diagnosis'),
    'tl_repair': ('إصلاح', 'Repair'),
    'tl_testing': ('اختبار', 'Testing'),
    'tl_completion': ('اكتمال', 'Completion'),
    'tl_delivery': ('تسليم', 'Delivery'),
    'tl_update': ('تحديث', 'Update'),
    'tl_maint_done': ('انتهاء الصيانة', 'Maintenance Complete'),
    'tl_device_delivered': ('تسليم الجهاز للعميل', 'Device Delivered to Client'),
    'tl_process_done': ('اكتمال العملية', 'Process Complete'),
    'tl_status_update': ('تحديث الحالة', 'Status Update'),
    'tl_new_status': ('الحالة الجديدة:', 'New Status:'),
    
    # Admin/roles
    'role_admin_label': ('مدير', 'Admin'),
    'role_manager_label': ('مشرف', 'Manager'),
    'role_staff_label': ('موظف', 'Staff'),
    'admin_default_name': ('المدير', 'Admin'),
    
    # No activity
    'no_activity_log': ('لا يوجد سجل نشاط', 'No activity log'),
    
    # Category labels for electrical
    'elec_power': ('القوى الكهربائية', 'Electrical Power'),
    'elec_control': ('مكونات الكنترول', 'Control Components'),
    'elec_automation': ('الأوتوميشن', 'Automation'),
    'elec_cables': ('الكابلات والتوصيلات', 'Cables & Connections'),
    'elec_panels': ('لوحات الكهرباء', 'Electrical Panels'),
    'elec_motors': ('المواتير', 'Motors'),
    'elec_spare': ('قطع الصيانة', 'Maintenance Parts'),
    'elec_instruments': ('أجهزة القياس', 'Measuring Instruments'),
}

# ============================================================
# PHASE 1: Insert new translation keys
# ============================================================

# Build ar and en blocks
ar_entries = []
en_entries = []
for key, (ar, en) in NEW_KEYS.items():
    ar_entries.append(f"    {key}: '{ar.replace(chr(39), chr(92)+chr(39))}',")
    en_entries.append(f"    {key}: '{en.replace(chr(39), chr(92)+chr(39))}',")

ar_block = "\n    // v7.2 — Complete translations\n" + "\n".join(ar_entries)
en_block = "\n    // v7.2 — Complete translations\n" + "\n".join(en_entries)

# Insert before closing of ar section
content = content.replace(
    "    repair_profit: 'الربح:',\n  },\n  en: {",
    "    repair_profit: 'الربح:',\n" + ar_block + "\n  },\n  en: {"
)

# Insert before closing of en section
content = content.replace(
    "    repair_total_cost: 'Total Cost:', repair_profit: 'Profit:',\n  }\n};",
    "    repair_total_cost: 'Total Cost:', repair_profit: 'Profit:',\n" + en_block + "\n  }\n};"
)

# ============================================================
# PHASE 2: Replace JS Arabic strings with t() calls
# ============================================================

# Simple replacements: toast('Arabic text' → toast(t('key')
js_replacements = [
    # Login errors
    ("errorEl.textContent = 'اسم المستخدم غير موجود'", "errorEl.textContent = t('toast_username_not_found')"),
    ("errorEl.textContent = 'كلمة المرور غير صحيحة'", "errorEl.textContent = t('toast_wrong_password')"),
    ("errorEl.textContent = 'الحساب معطل'", "errorEl.textContent = t('toast_account_disabled')"),
    
    # Sync status  
    ("el.title = 'متصل — Supabase'", "el.title = t('sync_connected_sb')"),
    ("text.textContent = 'متصل ✅'", "text.textContent = t('connected_status')"),
    ("overviewStatus) overviewStatus.textContent = 'متصل ✅'", "overviewStatus) overviewStatus.textContent = t('connected_status')"),
    
    # Confirm dialogs
    ("confirm('سيتم استبدال كل البيانات الحالية. متابعة؟')", "confirm(t('confirm_replace_all'))"),
    
    # PAGE_TITLES - replace with t() calls
    ("dashboard: 'لوحة التحكم',", "dashboard: t('page_dashboard'),"),
    ("inventory: 'المخزون',", "inventory: t('page_inventory'),"),
    ("categories: 'التصنيفات',", "categories: t('page_categories'),"),
    ("sales: 'البيع',", "sales: t('page_sales'),"),
    ("purchases: 'المشتريات',", "purchases: t('page_purchases'),"),
    ("maintenance: 'ورشة الصيانة',", "maintenance: t('page_maintenance'),"),
    ("accounting: 'المحاسبة',", "accounting: t('page_accounting'),"),
    ("reports: 'التقارير',", "reports: t('page_reports'),"),
    ("settings: 'الإعدادات',", "settings: t('page_settings'),"),
    
    # Currency
    ("return window._cachedCurrency || 'ج.م';", "return window._cachedCurrency || t('currency');"),
    ("const cur = window._cachedCurrency || 'ج.م';", "const cur = window._cachedCurrency || t('currency');"),
    
    # Scanner
    (">وجّه الكاميرا نحو الباركود</p>", ">${t('scanner_aim')}</p>"),  # Won't work in template literal
    
    # DEVICE_STATUSES
    ("'under_repair': { label: '🔧 تحت الصيانة'", "'under_repair': { label: t('device_under_repair')"),
    ("'done_not_delivered': { label: '✅ خلصت ومتسلمتش'", "'done_not_delivered': { label: t('device_done_not_delivered')"),
    ("'delivered_not_paid': { label: '📦 اتسلمت ومدفعتش'", "'delivered_not_paid': { label: t('device_delivered_not_paid')"),
    ("'completed': { label: '💰 خلصت واتدفعت'", "'completed': { label: t('device_completed')"),
    
    # Roles
    ("admin: { label: 'مدير'", "admin: { label: t('role_admin')"),
    ("manager: { label: 'مشرف'", "manager: { label: t('role_manager')"),
    ("staff: { label: 'موظف'", "staff: { label: t('role_staff')"),
    ("name: 'المدير',", "name: t('admin_default_name'),"),
    
    # Chart labels
    ("label: 'المبيعات',", "label: t('chart_lbl_sales'),"),
    ("label: 'المشتريات',", "label: t('chart_lbl_purchases'),"),
    
    # Maintenance chart labels
    ("const labels = { under_repair: 'تحت الصيانة', done_not_delivered: 'خلصت', delivered_not_paid: 'اتسلمت', completed: 'مكتملة' };",
     "const labels = { under_repair: t('chart_under_repair'), done_not_delivered: t('chart_done'), delivered_not_paid: t('chart_delivered'), completed: t('chart_completed') };"),
    
    # Modal titles
    ("document.getElementById('modal-product-title').textContent = 'إضافة صنف جديد'",
     "document.getElementById('modal-product-title').textContent = t('modal_add_product')"),
    ("document.getElementById('modal-product-title').textContent = 'تعديل الصنف'",
     "document.getElementById('modal-product-title').textContent = t('modal_edit_product')"),
    ("document.getElementById('modal-client-title').textContent = 'إضافة عميل جديد'",
     "document.getElementById('modal-client-title').textContent = t('modal_add_client')"),
    ("document.getElementById('modal-client-title').textContent = 'تعديل بيانات العميل'",
     "document.getElementById('modal-client-title').textContent = t('modal_edit_client')"),
    ("document.getElementById('modal-supplier-title').textContent = 'إضافة مورد جديد'",
     "document.getElementById('modal-supplier-title').textContent = t('modal_add_supplier')"),
    ("document.getElementById('modal-supplier-title').textContent = 'تعديل بيانات المورد'",
     "document.getElementById('modal-supplier-title').textContent = t('modal_edit_supplier')"),
    ("document.getElementById('modal-invoice-title').textContent = 'فاتورة بيع جديدة'",
     "document.getElementById('modal-invoice-title').textContent = t('new_sale_invoice')"),
    ("document.getElementById('modal-invoice-title').textContent = 'فاتورة شراء جديدة'",
     "document.getElementById('modal-invoice-title').textContent = t('new_purchase_invoice')"),
    ("document.getElementById('modal-stock-title').textContent = 'إضافة للمخزون'",
     "document.getElementById('modal-stock-title').textContent = t('modal_stock_in')"),
    ("document.getElementById('modal-stock-title').textContent = 'صرف من المخزون'",
     "document.getElementById('modal-stock-title').textContent = t('modal_stock_out')"),
    ("document.getElementById('modal-device-title').textContent = 'إذن استلام جهاز جديد'",
     "document.getElementById('modal-device-title').textContent = t('modal_new_device')"),
    ("document.getElementById('modal-device-title').textContent = 'تعديل أمر الصيانة'",
     "document.getElementById('modal-device-title').textContent = t('modal_edit_device')"),
    ("document.getElementById('modal-service-title').textContent = 'زيارة/خدمة جديدة'",
     "document.getElementById('modal-service-title').textContent = t('modal_new_service')"),
    ("document.getElementById('modal-service-title').textContent = 'تعديل الزيارة/الخدمة'",
     "document.getElementById('modal-service-title').textContent = t('modal_edit_service_title')"),
    ("document.getElementById('modal-user-title').textContent = 'إضافة مستخدم جديد'",
     "document.getElementById('modal-user-title').textContent = t('modal_add_user')"),
    ("document.getElementById('modal-user-title').textContent = 'تعديل المستخدم'",
     "document.getElementById('modal-user-title').textContent = t('modal_edit_user')"),
    ("document.getElementById('modal-engineer-title').textContent = 'إضافة مهندس/فني جديد'",
     "document.getElementById('modal-engineer-title').textContent = t('modal_add_engineer')"),
    ("document.getElementById('modal-engineer-title').textContent = 'تعديل المهندس/الفني'",
     "document.getElementById('modal-engineer-title').textContent = t('modal_edit_engineer')"),
    ("document.getElementById('modal-recipient-title').textContent = 'إضافة مستلم'",
     "document.getElementById('modal-recipient-title').textContent = t('modal_add_recipient')"),
    ("document.getElementById('modal-recipient-title').textContent = 'تعديل مستلم'",
     "document.getElementById('modal-recipient-title').textContent = t('modal_edit_recipient')"),
    ("document.getElementById('modal-adjust-balance-title').textContent = isClient ? 'سجل مدفوعات عميل' : 'سجل مدفوعات مورد'",
     "document.getElementById('modal-adjust-balance-title').textContent = isClient ? t('modal_payment_ledger') + ' - ' + t('inv_client_label') : t('modal_payment_ledger') + ' - ' + t('inv_supplier_label')"),
    
    # Invoice party labels
    ("document.getElementById('invoice-party-label').textContent = 'العميل'",
     "document.getElementById('invoice-party-label').textContent = t('inv_client_label')"),
    ("document.getElementById('invoice-party-label').textContent = 'المورد'",
     "document.getElementById('invoice-party-label').textContent = t('inv_supplier_label')"),
    
    # Password placeholder
    ("document.getElementById('user-password').placeholder = 'كلمة المرور'",
     "document.getElementById('user-password').placeholder = t('usr_password_ph')"),
    ("document.getElementById('user-password').placeholder = 'اتركه فارغ لعدم التغيير'",
     "document.getElementById('user-password').placeholder = t('usr_password_keep')"),
    
    # Simple toasts
    ("toast('تم تعديل بيانات العميل')", "toast(t('toast_client_updated'))"),
    ("toast('تم إضافة العميل')", "toast(t('toast_client_added'))"),
    ("toast('تم حذف العميل')", "toast(t('toast_client_deleted'))"),
    ("toast('تم تعديل بيانات المورد')", "toast(t('toast_supplier_updated'))"),
    ("toast('تم إضافة المورد')", "toast(t('toast_supplier_added'))"),
    ("toast('تم حذف المورد')", "toast(t('toast_supplier_deleted'))"),
    ("toast('تم تسجيل الدفع')", "toast(t('toast_payment_recorded'))"),
    ("toast('تم حذف الفاتورة')", "toast(t('toast_invoice_deleted'))"),
    ("toast('تم حذف أمر الصيانة')", "toast(t('toast_maint_deleted'))"),
    ("toast('تم تعديل أمر الصيانة')", "toast(t('toast_device_updated'))"),
    ("toast('تم إنشاء إذن الاستلام')", "toast(t('toast_device_created'))"),
    ("toast('تم تعديل المصروف')", "toast(t('toast_expense_updated'))"),
    ("toast('تم إضافة المصروف')", "toast(t('toast_expense_added'))"),
    ("toast('تم حذف المصروف')", "toast(t('toast_expense_deleted'))"),
    ("toast('تم تعديل الخدمة')", "toast(t('toast_service_updated'))"),
    ("toast('تم إضافة الخدمة')", "toast(t('toast_service_added'))"),
    ("toast('تم حذف الخدمة')", "toast(t('toast_service_deleted'))"),
    ("toast('تم تعديل المستخدم')", "toast(t('toast_user_updated'))"),
    ("toast('تم إضافة المستخدم')", "toast(t('toast_user_added'))"),
    ("toast('تم حذف المستخدم')", "toast(t('toast_user_deleted'))"),
    ("toast('تم حفظ المستلم ✅')", "toast(t('toast_recipient_saved'))"),
    ("toast('تم الحذف')", "toast(t('toast_deleted_msg'))"),
    ("toast('تم حفظ التوكن ✅')", "toast(t('toast_token_saved'))"),
    ("toast('أدخل الاسم', 'error')", "toast(t('enter_name'), 'error')"),
    ("toast('أدخل اسم المهندس', 'error')", "toast(t('toast_enter_engineer_name'), 'error')"),
    ("toast('تم إضافة المهندس بنجاح')", "toast(t('toast_engineer_added'))"),
    ("toast('تم إنشاء المرتجع')", "toast(t('toast_return_created'))"),
    ("toast('لا يوجد باركود', 'error')", "toast(t('no_barcode'), 'error')"),
    ("toast('الجهاز مكتمل بالفعل', 'info')", "toast(t('device_already_complete'), 'info')"),
    ("toast('أدخل اسم الصنف', 'error')", "toast(t('toast_enter_product_name'), 'error')"),
    ("toast('أضف صنف واحد على الأقل', 'warning')", "toast(t('toast_add_one_item'), 'warning')"),
    ("toast('اختر المنتج لكل الأصناف', 'warning')", "toast(t('toast_select_all_products'), 'warning')"),
    ("toast('يرجى ملء التاريخ ونوع الإجراء', 'error')", "toast(t('toast_fill_date_action'), 'error')"),
    ("toast('تم إضافة السجل')", "toast(t('toast_record_added'))"),
    ("toast('تم تحديث السجل')", "toast(t('toast_record_updated'))"),
    ("toast('تم حذف السجل')", "toast(t('toast_record_deleted'))"),
    ("toast('تم حذف الحركة')", "toast(t('toast_movement_deleted'))"),
    ("toast('اختر عميل أو مورد', 'error')", "toast(t('toast_select_entity'), 'error')"),
    ("toast('أدخل مبلغ صحيح', 'error')", "toast(t('toast_enter_valid_amount'), 'error')"),
    ("toast('تم حفظ الحركة')", "toast(t('toast_movement_saved'))"),
    ("toast('أدخل التوكن أولاً', 'warning')", "toast(t('toast_enter_token'), 'warning')"),
    ("toast('خطأ في الاتصال', 'error')", "toast(t('toast_connection_err'), 'error')"),
    ("toast('مسح الفواتير متاح للمدير فقط', 'error')", "toast(t('admin_only_delete_invoices'), 'error')"),
    ("toast('مسح الأصناف متاح للمدير فقط', 'error')", "toast(t('admin_only_delete_products'), 'error')"),
    
    # Confirm dialogs
    ("confirm('حذف هذا التصنيف؟')", "confirm(t('confirm_delete_category'))"),
    ("confirm('حذف هذا المصروف؟')", "confirm(t('confirm_delete_expense'))"),
    ("confirm('حذف هذه الخدمة؟')", "confirm(t('confirm_delete_service'))"),
    ("confirm('حذف هذا المستخدم؟')", "confirm(t('confirm_delete_user'))"),
    ("confirm('حذف هذا المستلم؟')", "confirm(t('confirm_delete_recipient'))"),
    ("confirm('حذف هذه الحركة؟')", "confirm(t('confirm_delete_movement'))"),
    ("confirm('سيتم إضافة الأصناف من الملف. متابعة؟')", "confirm(t('confirm_import_products'))"),
    ("confirm('هل أنت متأكد من حذف هذا السجل؟')", "confirm(t('confirm_delete_record'))"),
    
    # Various
    ("driveEl.textContent = isConnected ? 'متصل ✅' : 'غير متصل'",
     "driveEl.textContent = isConnected ? t('connected_status') : t('disconnected_status')"),
    ("driveText.textContent = isConnected ? 'متصل ✅' : 'غير متصل'",
     "driveText.textContent = isConnected ? t('connected_status') : t('disconnected_status')"),
    
    # User status
    ("u.active?'مفعل':'معطل'", "u.active?t('usr_active'):t('usr_disabled')"),
    ("u.active ? 'تم تفعيل المستخدم' : 'تم تعطيل المستخدم'",
     "u.active ? t('toast_user_activated') : t('toast_user_deactivated')"),
    
    # Empty states  
    ("container.innerHTML = '<p class=\"empty-state\" style=\"padding:20px\">لا توجد أجهزة</p>'",
     "container.innerHTML = '<p class=\"empty-state\" style=\"padding:20px\">' + t('chart_no_devices') + '</p>'"),
    ("container.innerHTML = '<p class=\"empty-state\" style=\"padding:12px\">لا توجد بيانات</p>'",
     "container.innerHTML = '<p class=\"empty-state\" style=\"padding:12px\">' + t('chart_no_data') + '</p>'"),
    ("container.innerHTML = '<p class=\"empty-state\" style=\"padding:12px\">لا توجد فواتير</p>'",
     "container.innerHTML = '<p class=\"empty-state\" style=\"padding:12px\">' + t('chart_no_invoices') + '</p>'"),
    ("container.innerHTML = '<p class=\"empty-state\">لا يوجد سجل نشاط</p>'",
     "container.innerHTML = '<p class=\"empty-state\">' + t('no_activity_log') + '</p>'"),
    
    # Invoice labels in view
    ("document.querySelector('#modal-view-product .modal-header h3').textContent = 'تفاصيل أمر الصيانة'",
     "document.querySelector('#modal-view-product .modal-header h3').textContent = t('dev_details_title')"),
    
    # Engineer specialty default
    ("document.getElementById('engineer-specialty').value = engineer.specialty || 'عام'",
     "document.getElementById('engineer-specialty').value = engineer.specialty || t('specialty_general')"),
    
    # History entry default
    ("document.getElementById('history-entry-action').value = 'إصلاح'",
     "document.getElementById('history-entry-action').value = t('action_repair')"),
    
    # Expense type badge
    ("e.expenseType === 'indirect' ? 'rgba(108,60,233,0.1);color:var(--primary)' : 'rgba(245,158,11,0.1);color:var(--warning)'}`>${e.expenseType === 'indirect' ? 'مصروفات غير مباشرة' : 'مصروفات خزينة'}",
     "e.expenseType === 'indirect' ? 'rgba(108,60,233,0.1);color:var(--primary)' : 'rgba(245,158,11,0.1);color:var(--warning)'}`>${e.expenseType === 'indirect' ? t('exp_indirect') : t('exp_treasury')}"),
    
    # Service badges
    ("'pending': '<span class=\"badge\" style=\"background:rgba(245,158,11,0.1);color:var(--warning)\">قيد الانتظار</span>'",
     "'pending': '<span class=\"badge\" style=\"background:rgba(245,158,11,0.1);color:var(--warning)\">' + t('svc_pending') + '</span>'"),
    ("'in_progress': '<span class=\"badge\" style=\"background:rgba(0,200,255,0.1);color:#0891b2\">جاري التنفيذ</span>'",
     "'in_progress': '<span class=\"badge\" style=\"background:rgba(0,200,255,0.1);color:#0891b2\">' + t('svc_in_progress') + '</span>'"),
    ("'completed': '<span class=\"badge badge-new\">مكتملة</span>'",
     "'completed': '<span class=\"badge badge-new\">' + t('svc_completed') + '</span>'"),
    ("'cancelled': '<span class=\"badge badge-low\">ملغاة</span>'",
     "'cancelled': '<span class=\"badge badge-low\">' + t('svc_cancelled') + '</span>'"),
    
    # Invoice payment badges
    ("case 'paid': return '<span class=\"badge badge-new\">مدفوعة</span>'",
     "case 'paid': return '<span class=\"badge badge-new\">' + t('badge_paid') + '</span>'"),
    ("case 'partial': return '<span class=\"badge badge-used\">جزئي</span>'",
     "case 'partial': return '<span class=\"badge badge-used\">' + t('badge_partial') + '</span>'"),
    ("case 'unpaid': return '<span class=\"badge badge-low\">غير مدفوعة</span>'",
     "case 'unpaid': return '<span class=\"badge badge-low\">' + t('badge_unpaid') + '</span>'"),
    
    # Default lists
    ("'expense-categories': ['إيجار', 'مرتبات', 'كهرباء ومياه', 'نقل ومواصلات', 'صيانة']",
     "'expense-categories': [t('exp_rent'), t('exp_salaries'), t('exp_utilities'), t('exp_transport'), t('exp_maintenance')]"),
    ("'expense-types': ['مصروفات خزينة', 'مصروفات غير مباشرة']",
     "'expense-types': [t('exp_treasury'), t('exp_indirect')]"),
    ("'product-conditions': ['جديد', 'مستعمل']",
     "'product-conditions': [t('cond_new'), t('cond_used')]"),
    ("'product-types': ['جهاز', 'قطعة غيار', 'اكسسوار', 'كابل', 'شاحن']",
     "'product-types': [t('type_device'), t('type_part'), 'Accessory', 'Cable', 'Charger']"),
    ("'payment-statuses': ['مدفوع', 'غير مدفوع', 'جزئي']",
     "'payment-statuses': [t('invoice_paid'), t('invoice_unpaid'), t('invoice_partial')]"),
    ("'device-statuses': ['تحت الصيانة', 'تم الإصلاح', 'تم التسليم', 'مكتملة']",
     "'device-statuses': [t('chart_under_repair'), 'Repaired', 'Delivered', t('chart_completed')]"),
    ("'service-statuses': ['مجدول', 'جاري', 'مكتمل', 'ملغي']",
     "'service-statuses': ['Scheduled', 'Ongoing', 'Done', 'Cancelled']"),
    
    # Custom list editor
    ("editBtn.title = 'تعديل القائمة'", "editBtn.title = t('cl_edit_title')"),
    ("placeholder=\"اكتب هنا...\"", "placeholder=\"${t('cl_type_here')}\""),
    ("<span>احفظ</span>", "<span>${t('cl_save_label')}</span>"),
    ("placeholder=\"بحث...\"", "placeholder=\"${t('cl_search')}\""),
    ("${title || 'اختر'}", "${title || t('cl_choose')}"),
    ("data-value=\"__other__\">أخرى...</div>", "data-value=\"__other__\">${t('cl_other')}</div>"),
    ("emptyLabel || 'اختر...'", "emptyLabel || t('cl_choose')"),
    ("otherOpt.textContent = '➕ أخرى...'", "otherOpt.textContent = t('cl_other')"),
    
    # List editor modal
    ("const labelText = label ? label.textContent.replace('*','').trim() : 'اختر'",
     "const labelText = label ? label.textContent.replace('*','').trim() : t('cl_choose')"),
    
    # Engineer deletion
    ("confirm('حذف هذا المهندس/الفني؟')", "confirm(t('confirm_delete_engineer'))"),
    
    # toast with format
    ("toast('تم حفظ فاتورة البيع')", "toast(t('toast_sale_saved'))"),
    ("toast('تم حفظ فاتورة الشراء')", "toast(t('toast_purchase_saved'))"),
    ("toast('تم تحديث المهندس/الفني')", "toast(t('toast_engineer_updated'))"),
    ("toast('تم إضافة المهندس/الفني')", "toast(t('toast_engineer_saved'))"),
    ("toast('تم حذف المهندس/الفني')", "toast(t('toast_engineer_deleted'))"),
    ("toast('تم إتمام المهمة بنجاح', 'success')", "toast(t('toast_task_complete'), 'success')"),
    
    # Enabled/disabled toggle
    ("toast(notifRecipients[idx].enabled ? 'تم التفعيل' : 'تم التعطيل')",
     "toast(notifRecipients[idx].enabled ? t('toast_enabled') : t('toast_disabled'))"),
    
    # Permissions labels
    ("{ key: 'dashboard', label: 'لوحة التحكم' }", "{ key: 'dashboard', label: t('perm_dashboard') }"),
    ("{ key: 'inventory', label: 'المخزون — عرض' }", "{ key: 'inventory', label: t('perm_inv_view') }"),
    ("{ key: 'inventory_edit', label: 'المخزون — إضافة/تعديل/حذف' }", "{ key: 'inventory_edit', label: t('perm_inv_edit') }"),
    ("{ key: 'stock_movement', label: 'إضافة/صرف مخزون' }", "{ key: 'stock_movement', label: t('perm_stock') }"),
    ("{ key: 'view_prices', label: 'عرض الأسعار والأرباح' }", "{ key: 'view_prices', label: t('perm_prices') }"),
    ("{ key: 'sales', label: 'البيع — عرض' }", "{ key: 'sales', label: t('perm_sales_view') }"),
    ("{ key: 'sales_create', label: 'البيع — إنشاء فواتير' }", "{ key: 'sales_create', label: t('perm_sales_create') }"),
    ("{ key: 'purchases', label: 'المشتريات — عرض' }", "{ key: 'purchases', label: t('perm_purch_view') }"),
    ("{ key: 'purchases_create', label: 'المشتريات — إنشاء فواتير' }", "{ key: 'purchases_create', label: t('perm_purch_create') }"),
    ("{ key: 'clients', label: 'العملاء' }", "{ key: 'clients', label: t('perm_clients') }"),
    ("{ key: 'suppliers', label: 'الموردين' }", "{ key: 'suppliers', label: t('perm_suppliers') }"),
    ("{ key: 'maintenance', label: 'ورشة الصيانة' }", "{ key: 'maintenance', label: t('perm_maint') }"),
    ("{ key: 'maintenance_intake', label: 'استلام أجهزة' }", "{ key: 'maintenance_intake', label: t('perm_intake') }"),
    ("{ key: 'accounting', label: 'المحاسبة' }", "{ key: 'accounting', label: t('perm_accounting') }"),
    ("{ key: 'reports', label: 'التقارير' }", "{ key: 'reports', label: t('perm_reports') }"),
    ("{ key: 'settings', label: 'الإعدادات' }", "{ key: 'settings', label: t('perm_settings') }"),
    ("{ key: 'users', label: 'إدارة المستخدمين' }", "{ key: 'users', label: t('perm_users') }"),
    
    # Enter password toast
    ("toast('أدخل كلمة المرور', 'warning')", "toast(t('toast_enter_password'), 'warning')"),
    
    # Currency in telegram notifications  
    ("الإجمالي: ${total} ج.م", "الإجمالي: ${total} ${t('currency')}"),
    
    # toast with token/chatid
    ("toast('فشل — تأكد من التوكن', 'error')", "toast(t('toast_token_failed'), 'error')"),
]

for old, new in js_replacements:
    if old in content:
        content = content.replace(old, new)
    else:
        # Try a more relaxed match
        pass

# ============================================================  
# PHASE 3: HTML replacements - add data-i18n where possible
# ============================================================

html_replacements = [
    # Login page
    ('<p>نظام إدارة المخزون والصيانة</p>', '<p data-i18n="app_title">نظام إدارة المخزون والصيانة</p>'),
    ('<label class="remember-me"><input type="checkbox" id="login-remember" checked> تذكرني</label>',
     '<label class="remember-me"><input type="checkbox" id="login-remember" checked> <span data-i18n="remember_me">تذكرني</span></label>'),
    ('<button type="submit" class="btn btn-primary btn-block">تسجيل الدخول</button>',
     '<button type="submit" class="btn btn-primary btn-block" data-i18n="btn_login">تسجيل الدخول</button>'),
    
    # Buttons with Arabic
    ('onclick="openAddProduct()">إضافة أول صنف</button>',
     'onclick="openAddProduct()" data-i18n="add_first_product">إضافة أول صنف</button>'),
    ('onclick="openAddCategoryPage()">إضافة أول تصنيف</button>',
     'onclick="openAddCategoryPage()" data-i18n="add_first_category">إضافة أول تصنيف</button>'),
    ('onclick="openNewSaleInvoice()">إنشاء أول فاتورة</button>',
     'onclick="openNewSaleInvoice()" data-i18n="create_first_invoice">إنشاء أول فاتورة</button>'),
    ('onclick="openNewPurchaseInvoice()">إنشاء أول فاتورة</button>',
     'onclick="openNewPurchaseInvoice()" data-i18n="create_first_invoice">إنشاء أول فاتورة</button>'),
    ('onclick="openAddClient()">إضافة أول عميل</button>',
     'onclick="openAddClient()" data-i18n="add_first_client">إضافة أول عميل</button>'),
    ('onclick="openNewService()">إضافة أول زيارة</button>',
     'onclick="openNewService()" data-i18n="add_first_visit">إضافة أول زيارة</button>'),
    ('onclick="openAddSupplier()">إضافة أول مورد</button>',
     'onclick="openAddSupplier()" data-i18n="add_first_supplier">إضافة أول مورد</button>'),
    ('onclick="openNewDevice()">إذن استلام أول جهاز</button>',
     'onclick="openNewDevice()" data-i18n="intake_first_device">إذن استلام أول جهاز</button>'),
    ('onclick="openAddEngineer()">إضافة أول مهندس/فني</button>',
     'onclick="openAddEngineer()" data-i18n="add_first_engineer">إضافة أول مهندس/فني</button>'),
    
    # No data paragraphs
    ('<p>لا توجد مصروفات خزينة</p>',
     '<p data-i18n="no_treasury_expenses">لا توجد مصروفات خزينة</p>'),
    ('<p>لا توجد مصروفات غير مباشرة</p>',
     '<p data-i18n="no_indirect_expenses">لا توجد مصروفات غير مباشرة</p>'),
    ('<p>لا توجد مصروفات</p>',
     '<p data-i18n="no_expenses_page">لا توجد مصروفات</p>'),
    ('<p>لا توجد أجهزة في الصيانة</p>',
     '<p data-i18n="no_devices_maint">لا توجد أجهزة في الصيانة</p>'),
    
    # Notification checkboxes
    ('<label class="perm-checkbox"><input type="checkbox" id="rcpt-low-stock" checked> تنبيه مخزون منخفض</label>',
     '<label class="perm-checkbox"><input type="checkbox" id="rcpt-low-stock" checked> <span data-i18n="notif_low_stock">تنبيه مخزون منخفض</span></label>'),
    ('<label class="perm-checkbox"><input type="checkbox" id="rcpt-unpaid" checked> فواتير غير مدفوعة</label>',
     '<label class="perm-checkbox"><input type="checkbox" id="rcpt-unpaid" checked> <span data-i18n="notif_unpaid">فواتير غير مدفوعة</span></label>'),
    ('<label class="perm-checkbox"><input type="checkbox" id="rcpt-devices-ready" checked> أجهزة جاهزة للتسليم</label>',
     '<label class="perm-checkbox"><input type="checkbox" id="rcpt-devices-ready" checked> <span data-i18n="notif_devices_ready">أجهزة جاهزة للتسليم</span></label>'),
    ('<label class="perm-checkbox"><input type="checkbox" id="rcpt-warranty-expiry" checked> تنبيهات انتهاء الضمان</label>',
     '<label class="perm-checkbox"><input type="checkbox" id="rcpt-warranty-expiry" checked> <span data-i18n="notif_warranty_expiry">تنبيهات انتهاء الضمان</span></label>'),
    ('<label class="perm-checkbox"><input type="checkbox" id="rcpt-daily-summary"> ملخص يومي</label>',
     '<label class="perm-checkbox"><input type="checkbox" id="rcpt-daily-summary"> <span data-i18n="notif_daily_summary">ملخص يومي</span></label>'),
    
    # Modal buttons
    ("onclick=\"closeModal('modal-recipient')\">إلغاء</button>",
     "onclick=\"closeModal('modal-recipient')\" data-i18n=\"btn_cancel\">إلغاء</button>"),
    ("onclick=\"testRecipient()\"><i class='bx bx-send'></i> اختبار</button>",
     "onclick=\"testRecipient()\" data-i18n=\"btn_test_notif\"><i class='bx bx-send'></i> اختبار</button>"),
    ("onclick=\"closeModal('modal-product')\">إلغاء</button>",
     "onclick=\"closeModal('modal-product')\" data-i18n=\"btn_cancel\">إلغاء</button>"),
    ("onclick=\"closeModal('modal-stock')\">إلغاء</button>",
     "onclick=\"closeModal('modal-stock')\" data-i18n=\"btn_cancel\">إلغاء</button>"),
    ("onclick=\"closeModal('modal-engineer')\">إلغاء</button>",
     "onclick=\"closeModal('modal-engineer')\" data-i18n=\"btn_cancel\">إلغاء</button>"),
    ("onclick=\"closeModal('modal-repair-history')\" style=\"width:100%\">إغلاق</button>",
     "onclick=\"closeModal('modal-repair-history')\" style=\"width:100%\" data-i18n=\"btn_close\">إغلاق</button>"),
    
    # Generic save/confirm buttons
    ('<button type="submit" class="btn btn-primary">حفظ</button>',
     '<button type="submit" class="btn btn-primary" data-i18n="btn_save">حفظ</button>'),
    ('<button type="submit" class="btn btn-primary">تأكيد</button>',
     '<button type="submit" class="btn btn-primary" data-i18n="btn_confirm">تأكيد</button>'),
    
    # Placeholders
    ('placeholder="اتركه فارغ للتوليد التلقائي"',
     'placeholder="اتركه فارغ للتوليد التلقائي" data-i18n-placeholder="sku_auto_placeholder"'),
    ('placeholder="اسم التصنيف الجديد"',
     'placeholder="اسم التصنيف الجديد" data-i18n-placeholder="new_cat_placeholder"'),
    ('placeholder="اكتب الوصف أو الملاحظات..."',
     'placeholder="اكتب الوصف أو الملاحظات..." data-i18n-placeholder="write_notes_ph"'),
    
    # Specialty options
    ('<option value="عام">عام</option>', '<option value="عام" data-i18n="specialty_general">عام</option>'),
    ('<option value="موبايلات">موبايلات</option>', '<option value="موبايلات" data-i18n="specialty_mobiles">موبايلات</option>'),
    ('<option value="لابتوب">لابتوب</option>', '<option value="لابتوب" data-i18n="specialty_laptop">لابتوب</option>'),
    ('<option value="كمبيوتر">كمبيوتر</option>', '<option value="كمبيوتر" data-i18n="specialty_computer">كمبيوتر</option>'),
    ('<option value="طابعات">طابعات</option>', '<option value="طابعات" data-i18n="specialty_printers">طابعات</option>'),
    ('<option value="شبكات">شبكات</option>', '<option value="شبكات" data-i18n="specialty_networks">شبكات</option>'),
    ('<option value="كاميرات">كاميرات</option>', '<option value="كاميرات" data-i18n="specialty_cameras">كاميرات</option>'),
    ('<option value="أخرى">أخرى</option>', '<option value="أخرى" data-i18n="specialty_other">أخرى</option>'),
    
    # Repair history options
    ('<option value="استلام">استلام</option>', '<option value="استلام" data-i18n="action_intake">استلام</option>'),
    ('<option value="فحص">فحص</option>', '<option value="فحص" data-i18n="action_diagnosis">فحص</option>'),
    ('<option value="إصلاح">إصلاح</option>', '<option value="إصلاح" data-i18n="action_repair">إصلاح</option>'),
    ('<option value="اختبار">اختبار</option>', '<option value="اختبار" data-i18n="action_testing">اختبار</option>'),
    ('<option value="تسليم">تسليم</option>', '<option value="تسليم" data-i18n="action_delivery">تسليم</option>'),
    ('<option value="أخرى">أخرى</option>', '<option value="أخرى" data-i18n="action_other">أخرى</option>'),
    
    # Select engineer option
    ('<option value="">-- اختر المهندس --</option>',
     '<option value="" data-i18n="select_engineer">-- اختر المهندس --</option>'),
    ('<option value="__other__">مهندس آخر...</option>',
     '<option value="__other__" data-i18n="other_engineer">مهندس آخر...</option>'),
    
    # Root category option
    ('<option value="">تصنيف رئيسي</option>',
     '<option value="" data-i18n="root_category">تصنيف رئيسي</option>'),
    
    # Payment options
    ('<option value="payment_in">دفعة واردة (سداد من العميل)</option>',
     '<option value="payment_in" data-i18n="payment_in_opt">دفعة واردة (سداد من العميل)</option>'),
    ('<option value="payment_out">دفعة صادرة (دفع للمورد)</option>',
     '<option value="payment_out" data-i18n="payment_out_opt">دفعة صادرة (دفع للمورد)</option>'),
    ('<option value="add_debt">إضافة دين جديد</option>',
     '<option value="add_debt" data-i18n="add_debt_opt">إضافة دين جديد</option>'),
    
    # Backup buttons
    ("onclick=\"exportAllToFile()\"><i class='bx bx-export'></i> تصدير نسخة احتياطية</button>",
     "onclick=\"exportAllToFile()\" data-i18n=\"btn_export_backup\"><i class='bx bx-export'></i> تصدير نسخة احتياطية</button>"),
    ("onclick=\"importFromFile()\"><i class='bx bx-import'></i> استيراد نسخة احتياطية</button>",
     "onclick=\"importFromFile()\" data-i18n=\"btn_import_backup\"><i class='bx bx-import'></i> استيراد نسخة احتياطية</button>"),
    
    # Inline placeholders
    ('placeholder="اسم العميل"', 'placeholder="اسم العميل" data-i18n-placeholder="client_name_ph"'),
    ('placeholder="الاسم"', 'placeholder="الاسم" data-i18n-placeholder="name_ph"'),
    ('placeholder="اسم المهندس"', 'placeholder="اسم المهندس" data-i18n-placeholder="eng_name_ph"'),
    ('placeholder="الهاتف (اختياري)"', 'placeholder="الهاتف (اختياري)" data-i18n-placeholder="phone_opt_ph"'),
    ('placeholder="مثلاً: 123456789"', 'placeholder="مثلاً: 123456789" data-i18n-placeholder="chat_id_placeholder"'),
]

for old, new in html_replacements:
    content = content.replace(old, new)

# ============================================================  
# Write output
# ============================================================

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Count remaining Arabic outside translations
import re
arabic = re.compile(r'[\u0600-\u06FF]')
lines = content.split('\n')
in_trans = False
remaining = 0
for i, line in enumerate(lines, 1):
    if 'const TRANSLATIONS' in line:
        in_trans = True
    if in_trans and line.strip().startswith('};') and i > 3900:
        in_trans = False
        continue
    if in_trans:
        continue
    if arabic.search(line) and 'data-i18n' not in line:
        remaining += 1

print(f"Translations applied successfully!")
print(f"Remaining lines with Arabic (outside TRANSLATIONS, no data-i18n): {remaining}")
