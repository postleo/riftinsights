/**
 * Summoner's Chronicle - Authentication JavaScript
 * Handles AWS Cognito authentication, magic links, and access keys
 */

(function() {
    'use strict';

    // Tab switching
    const authTabs = document.querySelectorAll('.auth-tab');
    const authForms = document.querySelectorAll('.auth-form-container');

    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;

            // Update active states
            authTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            authForms.forEach(form => {
                form.classList.remove('active');
                if (form.id === `${targetTab}-form`) {
                    form.classList.add('active');
                }
            });
        });
    });

    // Email authentication form
    const emailAuthForm = document.getElementById('emailAuthForm');
    if (emailAuthForm) {
        emailAuthForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const authLoading = document.getElementById('authLoading');
            const authError = document.getElementById('authError');
            const emailForm = document.getElementById('email-form');
            const emailSuccess = document.getElementById('emailSuccess');

            try {
                // Show loading state
                emailForm.style.display = 'none';
                authLoading.style.display = 'block';
                authError.style.display = 'none';

                // Call AWS Cognito to send magic link
                const response = await sendMagicLink(email);

                // Show success message
                authLoading.style.display = 'none';
                emailSuccess.style.display = 'block';
                document.getElementById('sentEmail').textContent = email;

            } catch (error) {
                console.error('Authentication error:', error);

                // Show error message
                authLoading.style.display = 'none';
                authError.style.display = 'block';
                document.getElementById('errorMessage').textContent =
                    error.message || 'Failed to send magic link. Please try again.';
            }
        });
    }

    // Access key upload form
    const accessKeyForm = document.getElementById('accessKeyForm');
    if (accessKeyForm) {
        const fileInput = document.getElementById('accessKeyFile');
        const fileUploadArea = document.getElementById('fileUploadArea');
        const fileNameDisplay = document.getElementById('fileName');

        // Drag and drop handlers
        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.style.borderColor = 'var(--gold-primary)';
        });

        fileUploadArea.addEventListener('dragleave', () => {
            fileUploadArea.style.borderColor = 'var(--glass-border)';
        });

        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.style.borderColor = 'var(--glass-border)';

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        // File input change handler
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });

        function handleFileSelect(file) {
            if (file && file.name.endsWith('.sumvault')) {
                fileNameDisplay.textContent = `Selected: ${file.name}`;
                fileNameDisplay.style.display = 'block';
            } else {
                showError('Please select a valid .sumvault file');
            }
        }

        accessKeyForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const file = fileInput.files[0];
            if (!file) {
                showError('Please select an access key file');
                return;
            }

            const authLoading = document.getElementById('authLoading');
            const authError = document.getElementById('authError');
            const accesskeyForm = document.getElementById('accesskey-form');

            try {
                // Show loading state
                accesskeyForm.style.display = 'none';
                authLoading.style.display = 'block';
                authError.style.display = 'none';

                // Read and validate access key
                const accessKey = await readAccessKeyFile(file);

                // Authenticate with access key
                await authenticateWithAccessKey(accessKey);

                // Redirect to dashboard
                window.location.href = 'dashboard.html';

            } catch (error) {
                console.error('Access key authentication error:', error);

                // Show error message
                authLoading.style.display = 'none';
                authError.style.display = 'block';
                document.getElementById('errorMessage').textContent =
                    error.message || 'Invalid access key. Please try again.';
            }
        });
    }

    // Summoner setup form
    const setupForm = document.getElementById('setupForm');
    if (setupForm) {
        setupForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const summonerName = document.getElementById('summonerName').value;
            const region = document.getElementById('region').value;

            try {
                // Link summoner account
                await linkSummonerAccount(summonerName, region);

                // Generate initial report
                await triggerReportGeneration();

                // Redirect to dashboard
                window.location.href = 'dashboard.html';

            } catch (error) {
                console.error('Setup error:', error);
                showError(error.message || 'Failed to link account. Please try again.');
            }
        });
    }

    // Helper functions
    async function sendMagicLink(email) {
        // Check if AWS config is available
        if (typeof AWS_CONFIG === 'undefined') {
            throw new Error('AWS configuration not loaded');
        }

        const response = await fetch(`${AWS_CONFIG.apiEndpoint}/auth/magic-link`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to send magic link');
        }

        return await response.json();
    }

    async function readAccessKeyFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = (e) => {
                try {
                    const accessKey = JSON.parse(e.target.result);
                    if (!accessKey.token || !accessKey.userId) {
                        reject(new Error('Invalid access key format'));
                    } else {
                        resolve(accessKey);
                    }
                } catch (error) {
                    reject(new Error('Failed to parse access key file'));
                }
            };

            reader.onerror = () => reject(new Error('Failed to read file'));
            reader.readAsText(file);
        });
    }

    async function authenticateWithAccessKey(accessKey) {
        if (typeof AWS_CONFIG === 'undefined') {
            throw new Error('AWS configuration not loaded');
        }

        const response = await fetch(`${AWS_CONFIG.apiEndpoint}/auth/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(accessKey)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Authentication failed');
        }

        const result = await response.json();

        // Store authentication token
        localStorage.setItem('authToken', result.token);
        localStorage.setItem('userId', result.userId);

        return result;
    }

    async function linkSummonerAccount(summonerName, region) {
        if (typeof AWS_CONFIG === 'undefined') {
            throw new Error('AWS configuration not loaded');
        }

        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
            throw new Error('Not authenticated');
        }

        const response = await fetch(`${AWS_CONFIG.apiEndpoint}/summoner/link`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                summonerName,
                region
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to link summoner account');
        }

        const result = await response.json();
        localStorage.setItem('summonerPuuid', result.puuid);
        localStorage.setItem('summonerName', summonerName);
        localStorage.setItem('region', region);

        return result;
    }

    async function triggerReportGeneration() {
        if (typeof AWS_CONFIG === 'undefined') {
            throw new Error('AWS configuration not loaded');
        }

        const authToken = localStorage.getItem('authToken');
        const summonerPuuid = localStorage.getItem('summonerPuuid');

        if (!authToken || !summonerPuuid) {
            throw new Error('Missing authentication or summoner information');
        }

        const response = await fetch(`${AWS_CONFIG.apiEndpoint}/report/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                playerPuuid: summonerPuuid,
                year: new Date().getFullYear()
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to generate report');
        }

        return await response.json();
    }

    function showError(message) {
        const authError = document.getElementById('authError');
        const errorMessage = document.getElementById('errorMessage');

        if (authError && errorMessage) {
            errorMessage.textContent = message;
            authError.style.display = 'block';
        } else {
            alert(message);
        }
    }

    // Check if magic link verification is in URL
    const urlParams = new URLSearchParams(window.location.search);
    const magicToken = urlParams.get('token');

    if (magicToken) {
        verifyMagicLink(magicToken);
    }

    async function verifyMagicLink(token) {
        const authLoading = document.getElementById('authLoading');
        const authError = document.getElementById('authError');

        try {
            authLoading.style.display = 'block';

            const response = await fetch(`${AWS_CONFIG.apiEndpoint}/auth/verify-magic-link`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });

            if (!response.ok) {
                throw new Error('Invalid or expired magic link');
            }

            const result = await response.json();

            // Store authentication
            localStorage.setItem('authToken', result.token);
            localStorage.setItem('userId', result.userId);

            // Check if summoner is linked
            if (result.summonerLinked) {
                window.location.href = 'dashboard.html';
            } else {
                // Show setup card
                document.querySelector('.auth-card').style.display = 'none';
                document.getElementById('setupCard').style.display = 'block';
            }

        } catch (error) {
            authLoading.style.display = 'none';
            showError(error.message || 'Failed to verify magic link');
        }
    }

    console.log('Authentication module initialized');
})();
