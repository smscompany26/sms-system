#!/usr/bin/env python3
"""Third pass: title attributes, prompts, and key template literal patterns"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Title attributes on buttons in JS
    ('title="عرض"', 'title="${t(\'btn_view\')}"'),
    ('title="تعديل"', 'title="${t(\'btn_edit\')}"'),
    ('title="حذف"', 'title="${t(\'btn_delete\')}"'),
    ('title="عرض/طباعة"', 'title="${t(\'btn_print_view\')}"'),
    ('title="تسجيل دفع"', 'title="${t(\'btn_record_payment\')}"'),
    ('title="إضافة مخزون"', 'title="${t(\'btn_add_stock\')}"'),
    ('title="صرف مخزون"', 'title="${t(\'btn_reduce_stock\')}"'),
    ('title="تاريخ الصيانة"', 'title="${t(\'modal_repair_history\')}"'),
    ('title="تغيير الحالة"', 'title="${t(\'confirm_status_change\')}"'),
    ('title="تفعيل/تعطيل"', 'title="${t(\'toast_enabled\')}"'),
    ('title="اختبار"', 'title="${t(\'btn_test_notif\')}"'),
    
    # HTML title attributes (static HTML)
    ('title="الوضع الليلي"', 'title="Dark Mode"'),
    ('title="المزامنة السحابية"', 'title="Cloud Sync"'),
    ('title="رسم بياني"', 'title="Line Chart"'),
    ('title="أعمدة"', 'title="Bar Chart"'),
    ('title="عرض قائمة"', 'title="List View"'),
    ('title="عرض البطاقات"', 'title="Card View"'),
    ('title="إدارة العملاء"', 'title="Manage Clients"'),
    
    # Prompts
    ("const name = prompt('اسم التصنيف الرئيسي الجديد:');",
     "const name = prompt(t('prompt_new_main_category'));"),
    ("const name = prompt(`إضافة تصنيف فرعي لـ \"${parentName}\":`);",
     "const name = prompt(t('prompt_add_subcategory').replace('{name}', parentName));"),
    ("const newName = prompt('تعديل اسم التصنيف:', cat.name);",
     "const newName = prompt(t('prompt_edit_category'), cat.name);"),
    
    # Payment prompt
    ("const amount = parseFloat(prompt(`المبلغ المتبقي: ${formatMoney(remaining)}\\nأدخل المبلغ المدفوع:`, remaining));",
     "const amount = parseFloat(prompt(t('remaining_amount') + ': ' + formatMoney(remaining) + '\\n' + t('enter_paid_amount'), remaining));"),
    
    # Product view labels in template literals
    ("<div class=\"view-label\">الكود</div>", "<div class=\"view-label\">${t('vw_code')}</div>"),
    ("<div class=\"view-label\">الاسم</div>", "<div class=\"view-label\">${t('vw_name')}</div>"),
    ("<div class=\"view-label\">الحالة</div>", "<div class=\"view-label\">${t('vw_condition')}</div>"),
    ("<div class=\"view-label\">النوع</div>", "<div class=\"view-label\">${t('vw_type')}</div>"),
    ("<div class=\"view-label\">التصنيف</div>", "<div class=\"view-label\">${t('vw_category')}</div>"),
    ("<div class=\"view-label\">الباركود</div>", "<div class=\"view-label\">${t('vw_barcode')}</div>"),
    ("<div class=\"view-label\">سعر الشراء</div>", "<div class=\"view-label\">${t('vw_buy_price')}</div>"),
    ("<div class=\"view-label\">سعر البيع</div>", "<div class=\"view-label\">${t('vw_sell_price')}</div>"),
    ("<div class=\"view-label\">الربح/وحدة</div>", "<div class=\"view-label\">${t('vw_profit_unit')}</div>"),
    ("<div class=\"view-label\">الكمية</div>", "<div class=\"view-label\">${t('vw_quantity')}</div>"),
    ("<div class=\"view-label\">الحد الأدنى</div>", "<div class=\"view-label\">${t('vw_min_stock')}</div>"),
    ("<div class=\"view-label\">الوصف</div>", "<div class=\"view-label\">${t('vw_description')}</div>"),
    ("<div class=\"view-label\">ملاحظات</div>", "<div class=\"view-label\">${t('vw_notes')}</div>"),
    ("<div class=\"view-label\">رقم الأمر</div>", "<div class=\"view-label\">${t('dv_order')}</div>"),
    ("<div class=\"view-label\">الجهاز</div>", "<div class=\"view-label\">${t('dv_device')}</div>"),
    ("<div class=\"view-label\">المواصفات</div>", "<div class=\"view-label\">${t('dv_specs')}</div>"),
    ("<div class=\"view-label\">المشكلة</div>", "<div class=\"view-label\">${t('dv_problem')}</div>"),
    ("<div class=\"view-label\">تاريخ الدخول</div>", "<div class=\"view-label\">${t('dv_intake_date')}</div>"),
    ("<div class=\"view-label\">العميل</div>", "<div class=\"view-label\">${t('dv_client')}</div>"),
    ("<div class=\"view-label\">مصنع العميل</div>", "<div class=\"view-label\">${t('dv_client_factory')}</div>"),
    ("<div class=\"view-label\">المهندس المسؤول</div>", "<div class=\"view-label\">${t('dv_engineer')}</div>"),
    ("<div class=\"view-label\">الضمان</div>", "<div class=\"view-label\">${t('dv_warranty')}</div>"),
    ("<div class=\"view-label\">حالة المهمة</div>", "<div class=\"view-label\">${t('task_status')}</div>"),
    ("<div class=\"view-label\">الموعد النهائي</div>", "<div class=\"view-label\">${t('task_deadline')}</div>"),
    ("<div class=\"view-label\">المكافأة</div>", "<div class=\"view-label\">${t('task_reward')}</div>"),
    ("<div class=\"view-label\">العقوبة</div>", "<div class=\"view-label\">${t('task_penalty')}</div>"),
    ("<div class=\"view-label\">الإنذارات</div>", "<div class=\"view-label\">${t('task_warnings')}</div>"),
    ("<div class=\"view-label\">تعليمات المهمة</div>", "<div class=\"view-label\">${t('task_instructions')}</div>"),
    ("<div class=\"view-label\">صور الجهاز</div>", "<div class=\"view-label\">${t('dev_photos')}</div>"),
    ("<div class=\"view-label\">الرصيد</div>", "<div class=\"view-label\">${t('vw_balance')}</div>"),
    ("<div class=\"view-label\">الإيميل</div>", "<div class=\"view-label\">${t('vw_email')}</div>"),
    ("<div class=\"view-label\">اسم المصنع</div>", "<div class=\"view-label\">${t('vw_factory_name')}</div>"),
    ("<div class=\"view-label\">مكان المصنع</div>", "<div class=\"view-label\">${t('vw_factory_location')}</div>"),
    ("<div class=\"view-label\">نشاط المصنع</div>", "<div class=\"view-label\">${t('vw_factory_activity')}</div>"),
    ("<div class=\"view-label\">التليفون</div>", "<div class=\"view-label\">${t('label_phone')}</div>"),
    
    # Condition/type in product view
    ("p.condition === 'new' ? 'جديد' : 'مستعمل'", "p.condition === 'new' ? t('vw_new') : t('vw_used')"),
    ("p.type === 'device' ? 'جهاز' : 'قطعة غيار'", "p.type === 'device' ? t('vw_device') : t('vw_spare_part')"),
    
    # Badge labels
    ("'<span class=\"badge badge-new\">جديد</span>'", "'<span class=\"badge badge-new\">' + t('vw_new') + '</span>'"),
    ("'<span class=\"badge badge-used\">مستعمل</span>'", "'<span class=\"badge badge-used\">' + t('vw_used') + '</span>'"),
    ("'<span class=\"badge badge-device\">جهاز</span>'", "'<span class=\"badge badge-device\">' + t('vw_device') + '</span>'"),
    ("'<span class=\"badge badge-part\">قطعة غيار</span>'", "'<span class=\"badge badge-part\">' + t('vw_spare_part') + '</span>'"),
    ("'<span class=\"badge badge-low\">مخزون منخفض</span>'", "'<span class=\"badge badge-low\">' + t('vw_low_stock') + '</span>'"),
    
    # Available label
    (">المتاح: <strong", ">${t('vw_available')}: <strong"),
    
    # Existing label
    (">موجود</span>", ">${t('vw_existing')}</span>"),
    
    # Print barcode
    (">طباعة باركود", ">${t('vw_print_barcode')}"),
    
    # Movement history
    ("سجل الحركات</h3>", "${t('vw_movement_history')}</h3>"),
    ("<th>التاريخ</th><th>النوع</th><th>الكمية</th><th>ملاحظات</th>",
     "<th>${t('th_date')}</th><th>${t('th_type')}</th><th>${t('vw_quantity')}</th><th>${t('vw_notes')}</th>"),
    ("'<span style=\"color:var(--success)\">إضافة</span>'", "'<span style=\"color:var(--success)\">' + t('vw_add') + '</span>'"),
    ("'<span style=\"color:var(--danger)\">صرف</span>'", "'<span style=\"color:var(--danger)\">' + t('vw_dispatch') + '</span>'"),
    
    # Filter/select options  
    ("filterEl.innerHTML = '<option value=\"\">كل التصنيفات</option>'",
     "filterEl.innerHTML = '<option value=\"\">' + t('cat_all_filter') + '</option>'"),
    ("formEl.innerHTML = '<option value=\"\">بدون تصنيف</option>'",
     "formEl.innerHTML = '<option value=\"\">' + t('cat_none') + '</option>'"),
    ("parentEl.innerHTML = '<option value=\"\">تصنيف رئيسي</option>'",
     "parentEl.innerHTML = '<option value=\"\">' + t('cat_root') + '</option>'"),
    ("list.innerHTML = '<p class=\"empty-state\">لا توجد تصنيفات بعد</p>'",
     "list.innerHTML = '<p class=\"empty-state\">' + t('cat_no_categories') + '</p>'"),
    
    # Category counts
    (">(${count} صنف)</span>", ">(${count} ${t('cat_items')})</span>"),
    (">(${cCount} صنف)</span>", ">(${cCount} ${t('cat_items')})</span>"),
    (">بدون تصنيف رئيسي<", ">${t('cat_no_parent')}<"),
    ("'<p class=\"empty-state\" style=\"padding:40px\">لا توجد نتائج</p>'",
     "'<p class=\"empty-state\" style=\"padding:40px\">' + t('cat_no_results') + '</p>'"),
    
    # Category page buttons
    ("><i class='bx bx-plus'></i> فرعي</button>",
     "><i class='bx bx-plus'></i> ${t('cat_sub_btn')}</button>"),
    (">${totalCount} صنف · ${children.length} تصنيف فرعي</span>",
     ">${totalCount} ${t('cat_items')} · ${children.length} ${t('cat_subcats')}</span>"),
    
    # Items count
    ("${inv.items?.length || 0} صنف", "${inv.items?.length || 0} ${t('inv_items_count')}"),
    
    # Invoice select options  
    ("sel.innerHTML = '<option value=\"\">اختر العميل</option>'",
     "sel.innerHTML = '<option value=\"\">' + t('inv_select_client') + '</option>'"),
    ("'<option value=\"__other__\">+ أخرى (إضافة عميل جديد)</option>'",
     "'<option value=\"__other__\">' + t('inv_other_client') + '</option>'"),
    ("sel.innerHTML = '<option value=\"\">اختر المورد</option>'",
     "sel.innerHTML = '<option value=\"\">' + t('inv_select_supplier') + '</option>'"),
    ("'<option value=\"__other__\">+ أخرى (إضافة مورد جديد)</option>'",
     "'<option value=\"__other__\">' + t('inv_other_supplier') + '</option>'"),
    ("'<option value=\"__other__\">+ أخرى</option>'",
     "'<option value=\"__other__\">' + t('inv_other_short') + '</option>'"),
    ("'<option value=\"__other__\">+ أخرى (إضافة مهندس جديد)</option>'",
     "'<option value=\"__other__\">' + t('other_add_engineer') + '</option>'"),
    ("'<option value=\"__other__\">+ أخرى (إضافة عميل جديد)</option>'",
     "'<option value=\"__other__\">' + t('inv_other_client') + '</option>'"),
    
    # Invoice form items
    ("<option value=\"\">اختر صنف</option>",
     "<option value=\"\">${t('inv_select_product')}</option>"),
    ("<option value=\"__other__\">+ أخرى (إضافة صنف جديد)</option>",
     "<option value=\"__other__\">${t('inv_other_product')}</option>"),
    ('placeholder="الكمية"', 'placeholder="${t(\'inv_qty_ph\')}"'),
    ('placeholder="السعر"', 'placeholder="${t(\'inv_price_ph\')}"'),
    
    # Inline product form
    (">إضافة صنف جديد</div>", ">${t('inv_add_product')}</div>"),
    ('placeholder="اسم الصنف *"', 'placeholder="${t(\'inv_prod_name\')}"'),
    ('placeholder="التكلفة"', 'placeholder="${t(\'inv_cost_ph\')}"'),
    ('placeholder="الكود (اختياري)"', 'placeholder="${t(\'inv_code_ph\')}"'),
    (">إلغاء</button>", ">${t('btn_cancel')}</button>"),
    ("><i class='bx bx-check'></i> حفظ وإضافة</button>", "><i class='bx bx-check'></i> ${t('inv_save_add')}</button>"),
    
    # Invoice view
    (">${isSale ? 'فاتورة بيع' : 'فاتورة شراء'}</h3>",
     ">${isSale ? t('inv_sale_title') : t('inv_purchase_title')}</h3>"),
    (">${isSale ? 'فاتورة بيع' : 'فاتورة شراء'}</h2>",
     ">${isSale ? t('inv_sale_title') : t('inv_purchase_title')}</h2>"),
    (">رقم: <strong>", ">${t('inv_number_label')}: <strong>"),
    (">التاريخ: ", ">${t('inv_date_label')}: "),
    ("<strong>${partyLabel}:</strong>", "<strong>${partyLabel}:</strong>"),
    
    # Invoice table headers  
    ("<th>#</th><th>الصنف</th><th>الكمية</th><th>السعر</th><th>الإجمالي</th>",
     "<th>#</th><th>${t('th_product')}</th><th>${t('vw_quantity')}</th><th>${t('inv_price_header')}</th><th>${t('inv_total_header')}</th>"),
    
    # Invoice totals
    ("><span>الإجمالي:</span>", "><span>${t('inv_total_header')}:</span>"),
    ("><span>المدفوع:</span>", "><span>${t('inv_paid_label')}:</span>"),
    ("><span>المتبقي:</span>", "><span>${t('inv_remaining_label')}:</span>"),
    
    # By/notes in invoice
    ("><i class='bx bx-user'></i> بواسطة:", "><i class='bx bx-user'></i> ${t('inv_by')}:"),
    ("><strong>ملاحظات:</strong>", "><strong>${t('inv_notes')}:</strong>"),
    
    # Print buttons
    ("><i class='bx bx-printer'></i> طباعة</button>", "><i class='bx bx-printer'></i> ${t('btn_print')}</button>"),
    ("><i class='bx bx-receipt'></i>", "><i class='bx bx-receipt'></i>"),
    
    # QR labels
    (">باركود الفاتورة</p>", ">${t('inv_barcode')}</p>"),
    (">QR للتحقق</p>", ">${t('inv_qr')}</p>"),
    (">${companyName} — ${companyPhone} · تم الإنشاء بواسطة نظام SMS</div>",
     ">${companyName} — ${companyPhone} · ${t('inv_sms_footer')}</div>"),
    (">شكراً لتعاملكم معنا</div>", ">${t('inv_thank_you')}</div>"),
    
    # Unspecified
    ("|| 'غير محدد'", "|| t('unspecified')"),
    ("|| 'غير معروف'", "|| t('chart_unknown')"),
    
    # Device labels in cards
    ("><strong>العميل</strong>", "><strong>${t('dv_client')}</strong>"),
    ("><strong>المهندس</strong>", "><strong>${t('dv_engineer')}</strong>"),
    ("><strong>تاريخ الدخول</strong>", "><strong>${t('dv_intake_date')}</strong>"),
    ("><strong>السعر</strong>", "><strong>${t('inv_price_header')}</strong>"),
    ("><strong>المشكلة:</strong>", "><strong>${t('dv_problem')}:</strong>"),
    
    # Order number in card
    (">رقم الأمر: <strong>", ">${t('dv_order')}: <strong>"),
    
    # Warranty badge
    ("'🛡️ ضمان '+d.warrantyMonths+' شهر'", "'🛡️ ' + t('dev_warranty') + ' ' + d.warrantyMonths + ' ' + t('dev_months')"),
    ("'🛡️ ضمان ' + d.warrantyMonths + ' شهر'", "'🛡️ ' + t('dev_warranty') + ' ' + d.warrantyMonths + ' ' + t('dev_months')"),
    (">ضمان ${d.warrantyMonths} شهر</span>", ">${t('dev_warranty')} ${d.warrantyMonths} ${t('dev_months')}</span>"),
    
    # No warranty
    ("'لا يوجد ضمان'", "t('dv_no_warranty')"),
    
    # Overdue
    (">متأخر!</span>", ">${t('dev_overdue')}</span>"),
    
    # From stock / external
    ("'من المخزون'", "t('dev_from_stock')"),
    ("'شراء خارجي'", "t('dev_external')"),
    ("'<span class=\"badge badge-new\">مخزون</span>'", "'<span class=\"badge badge-new\">' + t('parts_stock') + '</span>'"),
    ("'<span class=\"badge badge-used\">خارجي</span>'", "'<span class=\"badge badge-used\">' + t('parts_external') + '</span>'"),
    ("p.fromStock?'مخزون':'خارجي'", "p.fromStock?t('parts_stock'):t('parts_external')"),
    
    # Select part
    ("<option value=\"\">اختر قطعة</option>", "<option value=\"\">${t('dev_select_part')}</option>"),
    ('placeholder="اسم القطعة"', 'placeholder="${t(\'dev_part_name\')}"'),
    ('placeholder="المورد"', 'placeholder="${t(\'dev_supplier\')}"'),
    
    # Parts cost labels
    ("><span>تكلفة قطع المخزون:</span>", "><span>${t('parts_stock_cost')}</span>"),
    ("><span>تكلفة القطع الخارجية:</span>", "><span>${t('parts_ext_cost')}</span>"),
    ("><span>مصاريف إضافية:</span>", "><span>${t('parts_extra')}</span>"),
    ("><span>التكلفة الإجمالية:</span>", "><span>${t('parts_total_cost')}</span>"),
    ("><span>سعر البيع:</span>", "><span>${t('parts_sell_price')}</span>"),
    ("><span>الربح:</span>", "><span>${t('parts_profit')}</span>"),
    ("><span>تكلفة القطع:</span>", "><span>${t('parts_cost')}</span>"),
    
    # Parts used title
    (">القطع المستخدمة</h4>", ">${t('parts_used_title')}</h4>"),
    ("<th>القطعة</th><th>المصدر</th><th>الكمية</th><th>السعر</th><th>الإجمالي</th>",
     "<th>${t('parts_part')}</th><th>${t('parts_source')}</th><th>${t('vw_quantity')}</th><th>${t('inv_price_header')}</th><th>${t('inv_total_header')}</th>"),
    
    # QR maint label
    (">QR Code — أمر صيانة ${d.orderNumber}</p>", ">${t('dev_qr')} ${d.orderNumber}</p>"),
    (">QR — أمر صيانة ${d.orderNumber}</p>", ">${t('dev_qr')} ${d.orderNumber}</p>"),
    
    # Print buttons for device
    ("><i class='bx bx-printer'></i> طباعة الملصق</button>", "><i class='bx bx-printer'></i> ${t('dev_print_label')}</button>"),
    ("><i class='bx bx-printer'></i> طباعة إيصال</button>", "><i class='bx bx-printer'></i> ${t('dev_print_receipt')}</button>"),
    
    # Task details
    ("><i class='bx bx-task'></i> تفاصيل المهمة</h4>", "><i class='bx bx-task'></i> ${t('task_details')}</h4>"),
    ("><i class='bx bx-check-circle'></i> إتمام المهمة</button>", "><i class='bx bx-check-circle'></i> ${t('task_complete_btn')}</button>"),
    ("><i class='bx bx-error'></i> إنذار</button>", "><i class='bx bx-error'></i> ${t('task_warn_btn')}</button>"),
    ("><i class='bx bx-x-circle'></i> عقوبة</button>", "><i class='bx bx-x-circle'></i> ${t('task_penalize_btn')}</button>"),
    
    # Task status labels
    ("'pending': { label: 'في الانتظار'", "'pending': { label: t('task_pending')"),
    ("'assigned': { label: 'تم التخصيص'", "'assigned': { label: t('task_assigned')"),
    ("'completed': { label: 'مكتمل'", "'completed': { label: t('task_completed')"),
    ("'overdue': { label: 'متأخر'", "'overdue': { label: t('task_overdue')"),
    
    # Task assignment modal
    (">تم تخصيص المهمة</h3>", ">${t('task_assigned_title')}</h3>"),
    (">تم تخصيص الجهاز للمهندس</p>", ">${t('task_assigned_desc')}</p>"),
    ("><strong>المهندس:</strong>", "><strong>${t('dv_engineer')}:</strong>"),
    ("><strong>الجهاز:</strong> ${device.deviceName}", "><strong>${t('dv_device')}:</strong> ${device.deviceName}"),
    ("><strong>المشكلة:</strong> ${device.problem", "><strong>${t('dv_problem')}:</strong> ${device.problem"),
    ("><strong>الموعد النهائي:</strong>", "><strong>${t('task_deadline')}:</strong>"),
    ("><strong>تعليمات:</strong>", "><strong>${t('task_instructions')}:</strong>"),
    (">تم</button>", ">${t('btn_done')}</button>"),
    
    # Maintenance receipt labels  
    (">إيصال صيانة</h2>", ">${t('dev_receipt_title')}</h2>"),
    ("><strong>رقم الأمر:</strong>", "><strong>${t('dv_order')}:</strong>"),
    ("><strong>التاريخ:</strong>", "><strong>${t('inv_date_label')}:</strong>"),
    ("><strong>الحالة:</strong>", "><strong>${t('dv_status')}:</strong>"),
    ("><strong>العميل:</strong>", "><strong>${t('dv_client')}:</strong>"),
    ("><strong>الهاتف:</strong>", "><strong>${t('label_phone')}:</strong>"),
    ("><strong>الجهاز:</strong> ${d.deviceName}", "><strong>${t('dv_device')}:</strong> ${d.deviceName}"),
    ("><strong>المواصفات:</strong>", "><strong>${t('dv_specs')}:</strong>"),
    ("><strong>المشكلة:</strong> ${d.problem", "><strong>${t('dv_problem')}:</strong> ${d.problem"),
    
    # Report headers
    (">📊 التقرير اليومي — ", ">${t('rpt_daily')} — "),
    (">📊 التقرير الشهري — ", ">${t('rpt_monthly')} — "),
    (">📦 تقرير المخزون</h3>", ">${t('rpt_inventory')}</h3>"),
    (">💳 المبالغ المستحقة</h3>", ">${t('rpt_outstanding')}</h3>"),
    
    # Report section headers
    (">فواتير البيع (", ">${t('rpt_sale_invoices')} ("),
    (">فواتير الشراء (", ">${t('rpt_purchase_invoices')} ("),
    (">المصروفات (", ">${t('rpt_expenses')} ("),
    (">الصيانة</h3>", ">${t('rpt_maintenance')}</h3>"),
    (">تفصيل يومي</h3>", ">${t('rpt_daily_breakdown')}</h3>"),
    (">ملخص الصيانة</h3>", ">${t('rpt_maint_summary')}</h3>"),
    (">حسب التصنيف</h3>", ">${t('rpt_by_category')}</h3>"),
    
    # Report table headers
    ("<th>اليوم</th><th>المبيعات</th><th>المشتريات</th><th>المصروفات</th><th>الربح</th>",
     "<th>${t('rpt_day')}</th><th>${t('chart_lbl_sales')}</th><th>${t('chart_lbl_purchases')}</th><th>${t('rpt_expenses')}</th><th>${t('parts_profit')}</th>"),
    ("<th>التصنيف</th><th>عدد الأصناف</th><th>القيمة</th>",
     "<th>${t('vw_category')}</th><th>${t('rpt_item_count')}</th><th>${t('rpt_value')}</th>"),
    
    # Low stock header
    (">⚠️ أصناف منخفضة</h3>", ">${t('rpt_low_stock')}</h3>"),
    ("<th>الصنف</th><th>الكمية</th><th>الحد الأدنى</th>",
     "<th>${t('th_product')}</th><th>${t('vw_quantity')}</th><th>${t('vw_min_stock')}</th>"),
    
    # Outstanding table
    ("<th>الفاتورة</th><th>العميل</th><th>التاريخ</th><th>الإجمالي</th><th>المدفوع</th><th>المتبقي</th>",
     "<th>${t('th_invoice_num')}</th><th>${t('dv_client')}</th><th>${t('inv_date_label')}</th><th>${t('inv_total_header')}</th><th>${t('inv_paid_label')}</th><th>${t('inv_remaining_label')}</th>"),
    
    # Report empty states
    ("'<p class=\"empty-state\">لا توجد مبيعات</p>'", "'<p class=\"empty-state\">' + t('rpt_no_sales') + '</p>'"),
    ("'<p class=\"empty-state\">لا توجد مشتريات</p>'", "'<p class=\"empty-state\">' + t('rpt_no_purchases') + '</p>'"),
    ("'<p class=\"empty-state\">لا توجد مصروفات</p>'", "'<p class=\"empty-state\">' + t('rpt_no_expenses') + '</p>'"),
    
    # Devices in/out
    (">أجهزة دخلت: <strong>", ">${t('rpt_devices_in')}: <strong>"),
    (">أجهزة خلصت: <strong>", ">${t('rpt_devices_done')}: <strong>"),
    (">أجهزة مكتملة: <strong>", ">${t('rpt_devices_completed')}: <strong>"),
    
    # Outstanding total
    (">إجمالي المستحق</span>", ">${t('rpt_total_owed')}</span>"),
    
    # Accounting breakdown
    ("title = 'تفاصيل الإيرادات'", "title = t('acc_revenue_details')"),
    ("{ label: 'مبيعات',", "{ label: t('acc_sales'),"),
    ("{ label: 'صيانة',", "{ label: t('acc_maintenance'),"),
    ("{ label: 'خدمات وزيارات',", "{ label: t('acc_services'),"),
    ("title = 'تفاصيل المصروفات'", "title = t('acc_expenses_details')"),
    ("{ label: 'مشتريات',", "{ label: t('acc_purchases'),"),
    ("{ label: 'مصروفات عامة',", "{ label: t('acc_general_exp'),"),
    ("{ label: 'تكاليف صيانة',", "{ label: t('acc_maint_costs'),"),
    ("title = 'تفاصيل صافي الربح'", "title = t('acc_profit_details')"),
    ("{ label: 'إيراد المبيعات',", "{ label: t('acc_sales_rev'),"),
    ("{ label: 'ربح الصيانة',", "{ label: t('acc_maint_profit'),"),
    ("{ label: 'إيراد الخدمات',", "{ label: t('acc_services_rev'),"),
    ("{ label: 'المشتريات',", "{ label: t('acc_purchases'),"),
    ("{ label: 'المصروفات',", "{ label: t('rpt_expenses'),"),
    
    # This month
    ("هذا الشهر: <strong", "${t('chart_this_month')}: <strong"),
    (">هذا الشهر: ${formatMoney", ">${t('chart_this_month')}: ${formatMoney"),
    
    # Accounting no entities
    ("`<p class=\"empty-state\" style=\"padding:12px\">لا يوجد عملاء</p>",
     "`<p class=\"empty-state\" style=\"padding:12px\">${t('acc_no_clients')}</p>"),
    ("`<p class=\"empty-state\" style=\"padding:12px\">لا يوجد موردين</p>",
     "`<p class=\"empty-state\" style=\"padding:12px\">${t('acc_no_suppliers')}</p>"),
    
    # Record payment button
    ("><i class='bx bx-plus'></i> تسجيل دفعة</button>",
     "><i class='bx bx-plus'></i> ${t('acc_record_payment')}</button>"),
    
    # Ledger
    ("ledger.innerHTML = '<p class=\"empty-state\" style=\"padding:16px;font-size:13px\">لا توجد حركات مسجلة</p>'",
     "ledger.innerHTML = '<p class=\"empty-state\" style=\"padding:16px;font-size:13px\">' + t('ledger_no_movements') + '</p>'"),
    
    # Payment labels
    ("const label = isIn ? 'سداد' : isDebt ? 'دين' : p.type === 'payment_out' ? 'دفع' : 'تعديل'",
     "const label = isIn ? t('ledger_payment') : isDebt ? t('ledger_debt') : p.type === 'payment_out' ? t('ledger_pay_out') : t('ledger_adjustment')"),
    
    # Set balance title
    ("document.getElementById('adj-form-title').textContent = 'تسجيل دفعة جديدة'",
     "document.getElementById('adj-form-title').textContent = t('new_payment_title')"),
    ("document.getElementById('adj-form-title').textContent = 'تعيين الرصيد يدوياً'",
     "document.getElementById('adj-form-title').textContent = t('ledger_set_balance')"),
    ("document.getElementById('adj-pay-notes').value = 'تعديل يدوي'",
     "document.getElementById('adj-pay-notes').value = t('ledger_manual_adj')"),
    ("document.getElementById('adj-form-title').textContent = 'تعديل الحركة'",
     "document.getElementById('adj-form-title').textContent = t('ledger_edit')"),
    
    # Invoice reference in ledger
    ("' (فاتورة ' + p.invoiceNum + ')'", "' (' + t('ledger_invoice') + ' ' + p.invoiceNum + ')'"),
    
    # Select options
    ("sel.innerHTML = '<option value=\"\">اختر...</option>'",
     "sel.innerHTML = '<option value=\"\">' + t('cl_choose') + '...</option>'"),
    
    # Default option in engineer
    ("const defaultOption = '<option value=\"\">-- اختر المهندس --</option>'",
     "const defaultOption = '<option value=\"\">' + t('select_engineer') + '</option>'"),
    ("const otherOption = '<option value=\"__other__\">مهندس آخر...</option>'",
     "const otherOption = '<option value=\"__other__\">' + t('other_engineer') + '</option>'"),
    
    # Notification badge labels
    ("const notifLabels = { lowStock:'مخزون', unpaid:'فواتير', devicesReady:'تسليم', warrantyExpiry:'ضمان', dailySummary:'ملخص' }",
     "const notifLabels = { lowStock:t('notif_stock_badge'), unpaid:t('notif_inv_badge'), devicesReady:t('notif_delivery_badge'), warrantyExpiry:t('notif_warranty_badge'), dailySummary:t('notif_summary_badge') }"),
    
    # Enabled/disabled badge
    ("r.enabled !== false ? 'مفعل' : 'معطل'", "r.enabled !== false ? t('usr_active') : t('usr_disabled')"),
    
    # Timeline labels
    ("const actionLabels = { 'intake': 'استلام', 'diagnosis': 'فحص وتشخيص', 'repair': 'إصلاح', 'testing': 'اختبار', 'completed': 'اكتمال', 'delivered': 'تسليم' }",
     "const actionLabels = { 'intake': t('action_intake'), 'diagnosis': t('tl_diagnosis'), 'repair': t('action_repair'), 'testing': t('action_testing'), 'completed': t('tl_completion'), 'delivered': t('action_delivery') }"),
    
    # Status labels in timeline
    ("'done_not_delivered': 'انتهاء الصيانة'", "'done_not_delivered': t('tl_maint_done')"),
    ("'delivered_not_paid': 'تسليم الجهاز للعميل'", "'delivered_not_paid': t('tl_device_delivered')"),
    ("'completed': 'اكتمال العملية'", "'completed': t('tl_process_done')"),
    
    # Timeline titles
    ("title: 'استلام الجهاز',", "title: t('tl_intake'),"),
    ("statusLabels[device.status] || 'تحديث الحالة'", "statusLabels[device.status] || t('tl_status_update')"),
    ("entry.title || actionLabels[entry.action] || entry.action || 'تحديث'",
     "entry.title || actionLabels[entry.action] || entry.action || t('tl_update')"),
    
    # Device in timeline
    ("><strong>الجهاز:</strong> ${device.deviceName}", "><strong>${t('dv_device')}:</strong> ${device.deviceName}"),
    ("><strong>المشكلة:</strong> ${device.problem || 'غير محددة'}", "><strong>${t('dv_problem')}:</strong> ${device.problem || t('unspecified')}"),
    ("><strong>ملاحظات:</strong> ${device.notes}", "><strong>${t('vw_notes')}:</strong> ${device.notes}"),
    ("><strong>الحالة الجديدة:</strong>", "><strong>${t('tl_new_status')}</strong>"),
    ("><strong>سعر البيع:</strong>", "><strong>${t('parts_sell_price')}</strong>"),
    
    # Photo title
    ("title=\"انقر للعرض بالحجم الكامل\"", "title=\"Click to view full size\""),
    
    # Photos header
    ("><i class='bx bx-camera'></i> الصور المرفقة (", "><i class='bx bx-camera'></i> ${t('inv_photos')} ("),
    
    # Payment ledger title
    ("isClient ? 'سجل مدفوعات عميل' : 'سجل مدفوعات مورد'",
     "isClient ? t('modal_payment_ledger') + ' - ' + t('inv_client_label') : t('modal_payment_ledger') + ' - ' + t('inv_supplier_label')"),
    
    # Electrical categories (keep as data, but worth translating for display)
    ("{ name: 'القوى الكهربائية'", "{ name: t('elec_power')"),
    ("{ name: 'مكونات الكنترول'", "{ name: t('elec_control')"),
    ("{ name: 'الأوتوميشن'", "{ name: t('elec_automation')"),
    ("{ name: 'الكابلات والتوصيلات'", "{ name: t('elec_cables')"),
    ("{ name: 'لوحات الكهرباء'", "{ name: t('elec_panels')"),
    ("{ name: 'المواتير'", "{ name: t('elec_motors')"),
    ("{ name: 'قطع الصيانة'", "{ name: t('elec_spare')"),
    ("{ name: 'أجهزة القياس'", "{ name: t('elec_instruments')"),
    
    # No activity log
    ("container.innerHTML = '<p class=\"empty-state\">لا يوجد سجل نشاط</p>'",
     "container.innerHTML = '<p class=\"empty-state\">' + t('no_activity_log') + '</p>'"),
    
    # Activity log table headers
    ("<th>التاريخ</th><th>المستخدم</th><th>الإجراء</th><th>التفاصيل</th>",
     "<th>${t('th_date')}</th><th>${t('th_username')}</th><th>${t('th_actions')}</th><th>${t('th_description')}</th>"),
    
    # Category name fallback
    ("|| 'بدون تصنيف'", "|| t('cat_none')"),
    
    # Report table headers (invoice list)
    ("<th>الرقم</th><th>العميل</th><th>الإجمالي</th>",
     "<th>${t('th_num')}</th><th>${t('dv_client')}</th><th>${t('inv_total_header')}</th>"),
    ("<th>الرقم</th><th>المورد</th><th>الإجمالي</th>",
     "<th>${t('th_num')}</th><th>${t('inv_supplier_label')}</th><th>${t('inv_total_header')}</th>"),
    ("<th>البند</th><th>التصنيف</th><th>المبلغ</th>",
     "<th>${t('th_statement')}</th><th>${t('vw_category')}</th><th>${t('th_amount')}</th>"),
    
    # Accounting total label
    (">الإجمالي</span>", ">${t('acc_total')}</span>"),
    
    # Test data
    ("clientName: clients.length > 0 ? clients[0].name : 'عميل تجريبي'",
     "clientName: clients.length > 0 ? clients[0].name : t('test_client')"),
    ("notes: 'فاتورة اختبارية'", "notes: t('test_invoice_note')"),
    ("supplierName: suppliers.length > 0 ? suppliers[0].name : 'مورد تجريبي'",
     "supplierName: suppliers.length > 0 ? suppliers[0].name : t('test_supplier')"),
    ("notes: 'فاتورة شراء اختبارية'", "notes: t('test_purchase_note')"),
    
    # Return note
    ("notes: `مرتجع من فاتورة ${inv.number}`", "notes: t('return_from_invoice') + ' ' + inv.number"),
    
    # Currency in telegram
    ("ج.م`", "${t('currency')}`"),
    
    # Expense map
    ("const map = { 'مصروفات خزينة': 'treasury', 'مصروفات غير مباشرة': 'indirect' }",
     "const map = { [t('exp_treasury')]: 'treasury', [t('exp_indirect')]: 'indirect' }"),
    ("const map = { 'جديد': 'new', 'مستعمل': 'used' }",
     "const map = { [t('cond_new')]: 'new', [t('cond_used')]: 'used' }"),
    ("const map = { 'جهاز': 'device', 'قطعة غيار': 'part', 'اكسسوار': 'accessory', 'كابل': 'cable', 'شاحن': 'charger' }",
     "const map = { [t('type_device')]: 'device', [t('type_part')]: 'part', 'Accessory': 'accessory', 'Cable': 'cable', 'Charger': 'charger' }"),
    
    # Expense empty label
    ("emptyLabel: 'عام'", "emptyLabel: t('specialty_general')"),
    
    # Report date/month labels  
    ('>التاريخ:</label>', ' data-i18n="report_date_label">التاريخ:</label>'),
    ('>الشهر:</label>', ' data-i18n="report_month_label">الشهر:</label>'),
    
    # Inline client/invoice name placeholders - only match the specific ones
    ('id="new-client-device-name" placeholder="اسم العميل"',
     'id="new-client-device-name" placeholder="اسم العميل" data-i18n-placeholder="client_name_ph"'),
    ('id="new-client-invoice-name" placeholder="الاسم"',
     'id="new-client-invoice-name" placeholder="الاسم" data-i18n-placeholder="name_ph"'),
    ('id="new-client-service-name" placeholder="اسم العميل"',
     'id="new-client-service-name" placeholder="اسم العميل" data-i18n-placeholder="client_name_ph"'),
]

applied = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        applied += 1

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

print(f"Third pass complete. Applied {applied} replacements. Remaining: {remaining}")
