document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('subscriptionForm');
    const successMessage = document.getElementById('successMessage');
    const languageSelect = document.getElementById('language');
    
    // Element references for text that needs translation
    const formTitle = document.getElementById('formTitle');
    const formSubtitle = document.getElementById('formSubtitle');
    const nameLabel = document.getElementById('nameLabel');
    const emailLabel = document.getElementById('emailLabel');
    const languageLabel = document.getElementById('languageLabel');
    const selectOption = document.getElementById('selectOption');
    const submitButton = document.getElementById('submitButton');
    
    // Language translations
    const translations = {
        english: {
            title: 'Subscribe to Our Newsletter',
            subtitle: 'Stay updated with the latest AI News',
            nameLabel: 'Full Name',
            emailLabel: 'Email Address',
            languageLabel: 'Preferred Language',
            selectOption: 'Select your preferred language',
            submitButton: 'Subscribe Now',
            successMessage: 'Thank you for subscribing!',
            rtl: false
        },
        french: {
            title: 'Abonnez-vous à Notre Newsletter',
            subtitle: 'Restez informé des dernières nouvelles sur l\'IA',
            nameLabel: 'Nom Complet',
            emailLabel: 'Adresse Email',
            languageLabel: 'Langue Préférée',
            selectOption: 'Sélectionnez votre langue préférée',
            submitButton: 'S\'abonner Maintenant',
            successMessage: 'Merci de votre abonnement !',
            rtl: false
        },
        arabic: {
            title: 'اشترك في نشرتنا الإخبارية',
            subtitle: 'ابق على اطلاع بآخر أخبار الذكاء الاصطناعي',
            nameLabel: 'الاسم الكامل',
            emailLabel: 'البريد الإلكتروني',
            languageLabel: 'اللغة المفضلة',
            selectOption: 'اختر لغتك المفضلة',
            submitButton: 'اشترك الآن',
            successMessage: 'شكرا لاشتراكك!',
            rtl: true
        },
        darija: {
            title: 'شارك في نشرتنا الإخبارية',
            subtitle: 'بقى متبع آخر الأخبار ديال الذكاء الاصطناعي',
            nameLabel: 'الإسم الكامل',
            emailLabel: 'البريد الإلكتروني',
            languageLabel: 'اللغة المفضلة',
            selectOption: 'ختار اللغة المفضلة ديالك',
            submitButton: 'اشترك دابا',
            successMessage: 'شكرا على الاشتراك ديالك!',
            rtl: true
        }
    };

    // Apply translations based on selected language
    function applyTranslations(language) {
        // Default to English if the language is not found
        const currentTranslation = translations[language] || translations.english;
        
        // Update text content
        formTitle.textContent = currentTranslation.title;
        formSubtitle.textContent = currentTranslation.subtitle;
        nameLabel.textContent = currentTranslation.nameLabel;
        emailLabel.textContent = currentTranslation.emailLabel;
        languageLabel.textContent = currentTranslation.languageLabel;
        selectOption.textContent = currentTranslation.selectOption;
        submitButton.textContent = currentTranslation.submitButton;
        successMessage.textContent = currentTranslation.successMessage;
        
        // Handle RTL languages
        const elements = [document.body, form, nameLabel, emailLabel, languageLabel];
        
        if (currentTranslation.rtl) {
            elements.forEach(el => el.classList.add('rtl'));
            document.documentElement.setAttribute('lang', language);
            document.documentElement.setAttribute('dir', 'rtl');
        } else {
            elements.forEach(el => el.classList.remove('rtl'));
            document.documentElement.setAttribute('lang', language);
            document.documentElement.setAttribute('dir', 'ltr');
        }
    }
    
    // Form validation and submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Get form values
        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();
        const language = document.getElementById('language').value;
        const id = crypto.randomUUID();
        
        // Basic validation
        if (!fullName || !email || !language) {
            // Show error message in the selected language
            const currentLang = languageSelect.value || 'english';
            const errorMessages = {
                english: 'Please fill in all fields',
                french: 'Veuillez remplir tous les champs',
                arabic: 'يرجى ملء جميع الحقول',
                darija: 'عفاك عمر جميع الخانات'
            };
            
            alert(errorMessages[currentLang] || errorMessages.english);
            return;
        }
        
        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            // Show error message in the selected language
            const currentLang = languageSelect.value || 'english';
            const errorMessages = {
                english: 'Please enter a valid email address',
                french: 'Veuillez entrer une adresse email valide',
                arabic: 'يرجى إدخال عنوان بريد إلكتروني صالح',
                darija: 'دخل عنوان بريد إلكتروني صحيح'
            };
            
            alert(errorMessages[currentLang] || errorMessages.english);
            return;
        }
        
        // Here you would typically send the data to your server
        const formData = new URLSearchParams();
        formData.append('entry.481507162', fullName);
        formData.append('entry.1294968234', email);
        formData.append('entry.1698133956', language);
        formData.append('entry.377313160', id);

        fetch('https://docs.google.com/forms/d/e/1FAIpQLSdr1zKC9Pp9AsWFlBHvEe69EF549_O9udYuGZ3gqyPSnrbjxA/formResponse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()
        })
        .catch(error => {
            console.error('Error:', error);
        });
        
        // Show success message
        form.style.display = 'none';
        successMessage.style.display = 'block';
    });
    
    // Add input focus effects
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    // Language selection change handler
    languageSelect.addEventListener('change', function() {
        const selectedLanguage = this.value;
        applyTranslations(selectedLanguage);
    });
    
    // Initialize with English
    applyTranslations('english');
});