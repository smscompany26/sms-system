#!/usr/bin/env python3
"""Second pass: handle template literal toasts/confirms and remaining HTML"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Template literal toasts/confirms with variables
replacements = [
    # List editor delete
    ("if (!confirm(`حذف \"${item}\"؟`)) return;",
     "if (!confirm(t('confirm_delete_item').replace('{item}', item))) return;"),
    
    # Scanner
    ("toast('تم المسح: ' + code, 'info');",
     "toast(t('toast_scanned') + ': ' + code, 'info');"),
    ("if (confirm(`لم يتم العثور على منتج بباركود: ${code}\\nهل تريد إضافة منتج جديد؟`))",
     "if (confirm(t('confirm_product_not_found_add').replace('{code}', code)))"),
    ("toast(`تمت إضافة: ${found.name}`, 'success');",
     "toast(t('toast_added_item') + ': ' + found.name, 'success');"),
    
    # Delete product
    ("if (!confirm(`حذف الصنف \"${p?.name}\"؟`)) return;",
     "if (!confirm(t('confirm_delete_product').replace('{name}', p?.name))) return;"),
    
    # Stock qty
    ("return toast(`الكمية المتاحة ${product.quantity} فقط`, 'error');",
     "return toast(t('available_qty_only').replace('{qty}', product.quantity), 'error');"),
    ("toast(`تم ${actionLabel} ${qty} وحدة`);",
     "toast(t('toast_stock_done').replace('{action}', actionLabel).replace('{qty}', qty));"),
    
    # Import
    ("toast(`تم استيراد ${count} صنف`);",
     "toast(t('toast_imported_count').replace('{count}', count));"),
    
    # Category confirmations
    ("if (!confirm(`التصنيف \"${cat.name}\" له تصنيفات فرعية. حذف الكل؟`)) return;",
     "if (!confirm(t('confirm_delete_cat_children').replace('{name}', cat.name))) return;"),
    ("return toast(`لا يمكن حذف \"${child.name}\" لأنه يحتوي على أصناف`, 'error');",
     "return toast(t('cant_delete_has_products').replace('{name}', child.name), 'error');"),
    ("if (!confirm(`حذف التصنيف \"${cat.name}\"؟`)) return;",
     "if (!confirm(t('confirm_delete_cat').replace('{name}', cat.name))) return;"),
    
    # Client/Supplier deletes
    ("if (!confirm(`حذف العميل \"${c?.name}\"؟`)) return;",
     "if (!confirm(t('confirm_delete_client').replace('{name}', c?.name))) return;"),
    ("if (!confirm(`حذف المورد \"${s?.name}\"؟`)) return;",
     "if (!confirm(t('confirm_delete_supplier').replace('{name}', s?.name))) return;"),
    
    # Inline product added
    ("toast(`تم إضافة \"${name}\" ✅`);",
     "toast(t('toast_added_item') + ': ' + name + ' ✅');"),
    
    # Invoice save
    ("toast(type === 'sale' ? 'تم حفظ فاتورة البيع' : 'تم حفظ فاتورة الشراء');",
     "toast(type === 'sale' ? t('toast_sale_saved') : t('toast_purchase_saved'));"),
    
    # Bulk deletes
    ("if (!confirm(`حذف ${checked.length} فاتورة؟ سيتم إرجاع المخزون. لا يمكن التراجع!`)) return;",
     "if (!confirm(t('confirm_delete_invoices').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${ids.length} فاتورة`);",
     "toast(t('toast_deleted_invoices').replace('{count}', ids.length));"),
    ("if (!confirm(`حذف ${checked.length} عميل؟`)) return;",
     "if (!confirm(t('confirm_delete_clients').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${checked.length} عميل`);",
     "toast(t('toast_deleted_clients').replace('{count}', checked.length));"),
    ("if (!confirm(`حذف ${checked.length} مورد؟`)) return;",
     "if (!confirm(t('confirm_delete_suppliers').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${checked.length} مورد`);",
     "toast(t('toast_deleted_suppliers').replace('{count}', checked.length));"),
    ("if (!confirm(`حذف ${checked.length} خدمة؟`)) return;",
     "if (!confirm(t('confirm_delete_services').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${checked.length} خدمة`);",
     "toast(t('toast_deleted_services').replace('{count}', checked.length));"),
    ("if (!confirm(`حذف ${checked.length} جهاز؟`)) return;",
     "if (!confirm(t('confirm_delete_devices').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${checked.length} جهاز`);",
     "toast(t('toast_deleted_devices').replace('{count}', checked.length));"),
    ("if (!confirm(`حذف ${checked.length} مصروف؟`)) return;",
     "if (!confirm(t('confirm_delete_expenses').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${checked.length} مصروف`);",
     "toast(t('toast_deleted_expenses').replace('{count}', checked.length));"),
    ("if (!confirm(`حذف ${checked.length} مهندس؟`)) return;",
     "if (!confirm(t('confirm_delete_engineers').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${checked.length} مهندس`);",
     "toast(t('toast_deleted_engineers').replace('{count}', checked.length));"),
    ("if (!confirm(`حذف ${checked.length} صنف؟ لا يمكن التراجع!`)) return;",
     "if (!confirm(t('confirm_delete_products').replace('{count}', checked.length))) return;"),
    ("toast(`تم حذف ${ids.length} صنف`);",
     "toast(t('toast_deleted_products').replace('{count}', ids.length));"),
    ("if (!confirm(`حذف الفاتورة ${inv?.number}؟`)) return;",
     "if (!confirm(t('confirm_delete_invoice').replace('{num}', inv?.number))) return;"),
    
    # Client/supplier add
    ("toast(`تم إضافة ${isSupplier ? 'المورد' : 'العميل'} بنجاح`);",
     "toast(t('toast_client_supplier_added').replace('{type}', isSupplier ? t('inv_supplier_label') : t('inv_client_label')));"),
    ("if (!confirm(`حذف \"${entity.name}\"؟`)) return;",
     "if (!confirm(t('confirm_delete_entity').replace('{name}', entity.name))) return;"),
    ("toast(`تم حذف ${entity.name}`);",
     "toast(t('toast_entity_deleted').replace('{name}', entity.name));"),
    
    # Device assignment
    ("toast(`تم تخصيص الجهاز \"${device.deviceName}\" للمهندس ${engineer.name}`, 'success');",
     "toast(t('toast_device_assigned').replace('{device}', device.deviceName).replace('{engineer}', engineer.name), 'success');"),
    
    # Task completion
    ("toast(`تم إتمام المهمة في الوقت — مكافأة ${formatMoney(d.reward)} للمهندس ${engineer?.name}`, 'success');",
     "toast(t('toast_task_complete_ontime').replace('{amount}', formatMoney(d.reward)).replace('{engineer}', engineer?.name), 'success');"),
    ("toast(`تم إتمام المهمة (متأخر) — المهندس ${engineer?.name}`, 'warning');",
     "toast(t('toast_task_complete_late').replace('{engineer}', engineer?.name), 'warning');"),
    
    # Warnings
    ("toast(`تم إرسال إنذار ${d.warningsCount}/${d.warningsLimit} للمهندس ${engineer?.name}`, 'warning');",
     "toast(t('toast_warning_sent').replace('{count}', d.warningsCount).replace('{limit}', d.warningsLimit).replace('{engineer}', engineer?.name), 'warning');"),
    
    # Penalty
    ("if (!confirm(`تطبيق عقوبة ${formatMoney(d.penalty)} على المهندس ${engineer?.name}؟`)) return;",
     "if (!confirm(t('confirm_penalty').replace('{amount}', formatMoney(d.penalty)).replace('{engineer}', engineer?.name))) return;"),
    ("toast(`تم تطبيق العقوبة ${formatMoney(d.penalty)} على المهندس ${engineer?.name}`, 'error');",
     "toast(t('toast_penalty_applied').replace('{amount}', formatMoney(d.penalty)).replace('{engineer}', engineer?.name), 'error');"),
    
    # Delete maintenance order
    ("if (!confirm(`حذف أمر الصيانة ${d?.orderNumber}؟`)) return;",
     "if (!confirm(t('confirm_delete_maint_order').replace('{num}', d?.orderNumber))) return;"),
    
    # Status change
    ("if (!confirm(`تغيير الحالة إلى: ${nextLabel}؟`)) return;",
     "if (!confirm(t('confirm_status_change').replace('{status}', nextLabel))) return;"),
    ("toast(`تم تغيير الحالة إلى ${nextLabel}`);",
     "toast(t('toast_status_changed').replace('{status}', nextLabel));"),
    
    # Engineer delete with devices
    ("if (!confirm(`هذا المهندس/الفني مسؤول عن ${assignedDevices.length} جهاز. هل تريد المتابعة؟`)) return;",
     "if (!confirm(t('confirm_engineer_has_devices').replace('{count}', assignedDevices.length))) return;"),
    
    # Telegram
    ("toast(`تم العثور على ${chatList.length} محادثة`);",
     "toast(t('toast_found_chats').replace('{count}', chatList.length));"),
    ("toast(`تم نسخ Chat ID: ${chatId}`);",
     "toast(t('toast_chat_id_copied') + ': ' + chatId);"),
    ("return toast('أدخل التوكن و Chat ID', 'warning');",
     "return toast(t('toast_enter_token_chatid'), 'warning');"),
    ("toast(ok ? 'تم الإرسال ✅' : 'فشل — تحقق من Chat ID', ok ? 'success' : 'error');",
     "toast(ok ? t('toast_sent_success') : t('toast_check_chatid'), ok ? 'success' : 'error');"),
    ("return toast('تحقق من التوكن و Chat ID', 'warning');",
     "return toast(t('toast_check_token_chatid'), 'warning');"),
    ("toast(ok ? `تم الإرسال لـ ${r.name} ✅` : 'فشل — تحقق من Chat ID', ok ? 'success' : 'error');",
     "toast(ok ? t('toast_sent_success') + ' ' + r.name : t('toast_check_chatid'), ok ? 'success' : 'error');"),
    ("toast('تم إرسال اختبار لكل المستلمين ✅');",
     "toast(t('toast_test_all_sent'));"),
    
    # Test data
    ("toast('تم إضافة ' + testData.length + ' فاتورة اختبارية ✅');",
     "toast(t('toast_test_data_added').replace('{count}', testData.length));"),
    
    # Some remaining HTML table headers without data-i18n
    ('<th>رقم الفاتورة</th><th>التاريخ</th><th>العميل</th><th>الأصناف</th><th>الإجمالي</th><th>الحالة</th><th>بواسطة</th><th>إجراءات</th>',
     '<th data-i18n="th_invoice_num">رقم الفاتورة</th><th data-i18n="th_date">التاريخ</th><th data-i18n="th_client">العميل</th><th data-i18n="th_items">الأصناف</th><th data-i18n="th_total">الإجمالي</th><th data-i18n="th_status">الحالة</th><th data-i18n="th_by">بواسطة</th><th data-i18n="th_actions">إجراءات</th>'),
    ('<th>رقم الفاتورة</th><th>التاريخ</th><th>المورد</th><th>الأصناف</th><th>الإجمالي</th><th>الحالة</th><th>بواسطة</th><th>إجراءات</th>',
     '<th data-i18n="th_invoice_num">رقم الفاتورة</th><th data-i18n="th_date">التاريخ</th><th>المورد</th><th data-i18n="th_items">الأصناف</th><th data-i18n="th_total">الإجمالي</th><th data-i18n="th_status">الحالة</th><th data-i18n="th_by">بواسطة</th><th data-i18n="th_actions">إجراءات</th>'),
    ('<thead><tr><th>الاسم</th><th>Chat ID</th><th>الإشعارات</th><th>الحالة</th><th>إجراءات</th></tr></thead>',
     '<thead><tr><th data-i18n="th_name">الاسم</th><th>Chat ID</th><th data-i18n="th_notifications">الإشعارات</th><th data-i18n="th_status">الحالة</th><th data-i18n="th_actions">إجراءات</th></tr></thead>'),
    ('<thead><tr><th>الاسم</th><th>اسم المستخدم</th><th>الدور</th><th>الحالة</th><th>إجراءات</th></tr></thead>',
     '<thead><tr><th data-i18n="th_name">الاسم</th><th data-i18n="th_username">اسم المستخدم</th><th data-i18n="th_role">الدور</th><th data-i18n="th_status">الحالة</th><th data-i18n="th_actions">إجراءات</th></tr></thead>'),
    
    # Repair history strong labels
    ('<strong>الأمر:</strong>', '<strong data-i18n="order_colon">الأمر:</strong>'),
    ('<strong>الجهاز:</strong>', '<strong data-i18n="device_colon">الجهاز:</strong>'),
    ('<strong>العميل:</strong>', '<strong data-i18n="client_colon">العميل:</strong>'),
    ('<strong>الدخول:</strong>', '<strong data-i18n="intake_colon">الدخول:</strong>'),
    
    # Record add button
    ("<i class='bx bx-plus'></i> إضافة سجل", "<i class='bx bx-plus'></i> <span data-i18n=\"add_record_btn\">إضافة سجل</span>"),
    
    # History form labels
    ('<label>التاريخ</label>', '<label data-i18n="date_label">التاريخ</label>'),
    
    # Save/cancel in history
    ("onclick=\"saveHistoryEntry()\">حفظ</button>",
     "onclick=\"saveHistoryEntry()\" data-i18n=\"btn_save\">حفظ</button>"),
    ("onclick=\"cancelHistoryEntry()\">إلغاء</button>",
     "onclick=\"cancelHistoryEntry()\" data-i18n=\"btn_cancel\">إلغاء</button>"),
    
    # Export section headers
    ("<h4><i class='bx bx-export'></i> تصدير</h4>",
     "<h4><i class='bx bx-export'></i> <span data-i18n=\"export_section\">تصدير</span></h4>"),
    ("<h4><i class='bx bx-import'></i> استيراد</h4>",
     "<h4><i class='bx bx-import'></i> <span data-i18n=\"import_section\">استيراد</span></h4>"),
    ("<p>تصدير كل الأصناف إلى ملف Excel</p>",
     "<p data-i18n=\"export_products_desc\">تصدير كل الأصناف إلى ملف Excel</p>"),
    ("<p>استيراد أصناف من ملف Excel (يجب أن يتبع نفس التنسيق)</p>",
     "<p data-i18n=\"import_products_desc\">استيراد أصناف من ملف Excel (يجب أن يتبع نفس التنسيق)</p>"),
    
    # Permissions text
    ('<strong>الصلاحيات:</strong>', '<strong data-i18n="permissions_title">الصلاحيات:</strong>'),
    ('<strong>مدير:</strong> كل شيء — تحكم كامل',
     '<strong data-i18n="role_admin">مدير</strong>: <span data-i18n="role_admin_full">كل شيء — تحكم كامل</span>'),
    ('<strong>مشرف:</strong> المخزون + الفواتير + الصيانة + التقارير + الأسعار',
     '<strong data-i18n="role_manager">مشرف</strong>: <span data-i18n="role_manager_full">المخزون + الفواتير + الصيانة + التقارير + الأسعار</span>'),
    ('<strong>موظف:</strong> إنشاء فواتير + إضافة/صرف مخزون + استلام أجهزة — بدون أسعار أو أرباح',
     '<strong data-i18n="role_staff">موظف</strong>: <span data-i18n="role_staff_full">إنشاء فواتير + إضافة/صرف مخزون + استلام أجهزة — بدون أسعار أو أرباح</span>'),
    
    # Drive status  
    ('<span id="drive-status-text">غير متصل</span>',
     '<span id="drive-status-text" data-i18n="sync_not_connected">غير متصل</span>'),
    
    # Backup descriptions
    ('>المزامنة تعمل تلقائياً — كل التعديلات تتزامن بين جميع الأجهزة</p>',
     ' data-i18n="sync_auto_desc">المزامنة تعمل تلقائياً — كل التعديلات تتزامن بين جميع الأجهزة</p>'),
    ('>تصدير/استيراد كل بيانات النظام كملف JSON على جهازك</p>',
     ' data-i18n="backup_desc">تصدير/استيراد كل بيانات النظام كملف JSON على جهازك</p>'),
    
    # Telegram instructions
    ('يبعت أي رسالة للبوت على Telegram (مثلاً /start) → ثم دوس "جلب Chat IDs" هنا → هيظهر الـ Chat ID تلقائي',
     '<span data-i18n="telegram_instructions">يبعت أي رسالة للبوت على Telegram (مثلاً /start) → ثم دوس "جلب Chat IDs" هنا → هيظهر الـ Chat ID تلقائي</span>'),
    
    # Phone placeholder (multiple instances) 
    ('placeholder="الهاتف"', 'placeholder="الهاتف" data-i18n-placeholder="phone_ph"'),
    
    # Save inline button
    ("""onclick="saveInlineClient('device')" style="white-space:nowrap"><i class='bx bx-check'></i> حفظ</button>""",
     """onclick="saveInlineClient('device')" style="white-space:nowrap" data-i18n="btn_save"><i class='bx bx-check'></i> حفظ</button>"""),
    ("""onclick="saveInlineClient('invoice')" style="white-space:nowrap"><i class='bx bx-check'></i> حفظ</button>""",
     """onclick="saveInlineClient('invoice')" style="white-space:nowrap" data-i18n="btn_save"><i class='bx bx-check'></i> حفظ</button>"""),
    ("""onclick="saveInlineClient('service')" style="white-space:nowrap"><i class='bx bx-check'></i> حفظ</button>""",
     """onclick="saveInlineClient('service')" style="white-space:nowrap" data-i18n="btn_save"><i class='bx bx-check'></i> حفظ</button>"""),
    ("""onclick="saveInlineEngineer()" style="white-space:nowrap"><i class='bx bx-check'></i> حفظ</button>""",
     """onclick="saveInlineEngineer()" style="white-space:nowrap" data-i18n="btn_save"><i class='bx bx-check'></i> حفظ</button>"""),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Recount
import re
arabic = re.compile(r'[\u0600-\u06FF]')
lines = content.split('\n')
in_trans = False
remaining = 0
for i, line in enumerate(lines, 1):
    if 'const TRANSLATIONS' in line: in_trans = True
    if in_trans and line.strip().startswith('};') and i > 3900: in_trans = False; continue
    if in_trans: continue
    if arabic.search(line) and 'data-i18n' not in line:
        remaining += 1
print(f"Second pass complete. Remaining: {remaining}")
