/**
 * Summoner's Chronicle - Dashboard JavaScript
 * Handles navigation, data loading, and UI updates
 */

(function() {
    'use strict';

    let userData = null;
    let reportData = null;

    // Initialize dashboard
    async function initDashboard() {
        // Check authentication
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
            window.location.href = 'auth.html';
            return;
        }

        // Load user data and report
        try {
            await loadUserData();
            await loadReportData();
            setupNavigation();
            setupActions();
        } catch (error) {
            console.error('Dashboard initialization error:', error);
            if (error.message === 'Unauthorized') {
                localStorage.clear();
                window.location.href = 'auth.html';
            }
        }
    }

    // Load user data
    async function loadUserData() {
        const authToken = localStorage.getItem('authToken');
        const response = await fetch(`${AWS_CONFIG.apiEndpoint}/user/profile`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Unauthorized');
            }
            throw new Error('Failed to load user data');
        }

        userData = await response.json();

        // Update header
        document.getElementById('summonerName').textContent = userData.summonerName || 'Loading...';
        document.getElementById('currentRank').textContent = userData.rank || 'Unranked';
    }

    // Load report data from RiftSage
    async function loadReportData() {
        const authToken = localStorage.getItem('authToken');
        const summonerPuuid = localStorage.getItem('summonerPuuid');

        const response = await fetch(
            `${AWS_CONFIG.apiEndpoint}/report/${summonerPuuid}?year=${new Date().getFullYear()}`,
            {
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            }
        );

        if (!response.ok) {
            throw new Error('Failed to load report data');
        }

        reportData = await response.json();

        // Populate all sections with data
        populateOverview();
        populatePerformance();
        populateChampions();
        populateTeamImpact();
        populateGrowth();
        populateAchievements();
        populateFutureGoals();
    }

    // Setup navigation
    function setupNavigation() {
        const navPills = document.querySelectorAll('.nav-pill');
        const contentSections = document.querySelectorAll('.content-section');

        navPills.forEach(pill => {
            pill.addEventListener('click', () => {
                const sectionId = pill.dataset.section;

                // Update active states
                navPills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');

                contentSections.forEach(section => {
                    section.classList.remove('active');
                    if (section.id === sectionId) {
                        section.classList.add('active');
                    }
                });

                // Smooth scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        });
    }

    // Setup header actions
    function setupActions() {
        // Download button
        document.getElementById('downloadBtn').addEventListener('click', downloadReport);

        // Share button
        document.getElementById('shareBtn').addEventListener('click', shareReport);

        // Settings button
        document.getElementById('settingsBtn').addEventListener('click', () => {
            // TODO: Implement settings modal
            console.log('Settings clicked');
        });

        // Logout button
        document.getElementById('logoutBtn').addEventListener('click', logout);
    }

    // Populate overview section
    function populateOverview() {
        if (!reportData || !reportData.overview) return;

        const overview = reportData.overview;

        // Update stats
        document.getElementById('totalGames').textContent = overview.totalGames || '-';
        document.getElementById('winRate').textContent = `${overview.winRate || 0}%`;
        document.getElementById('avgKDA').textContent = overview.avgKDA?.toFixed(2) || '-';
        document.getElementById('mainRole').textContent = overview.mainRole || '-';

        // Update insights
        const insightsList = document.getElementById('overviewInsights');
        if (overview.insights && overview.insights.length > 0) {
            insightsList.innerHTML = overview.insights
                .map(insight => `<li><i class="fas fa-circle"></i> <span>${insight}</span></li>`)
                .join('');
        }

        // Update narrative
        document.getElementById('overviewNarrative').textContent =
            overview.narrative || 'Your personalized narrative will appear here...';
    }

    // Populate performance section
    function populatePerformance() {
        if (!reportData || !reportData.performance) return;

        const perf = reportData.performance;

        // Update stats
        document.getElementById('avgKills').textContent = perf.avgKills?.toFixed(1) || '-';
        document.getElementById('avgAssists').textContent = perf.avgAssists?.toFixed(1) || '-';
        document.getElementById('avgDeaths').textContent = perf.avgDeaths?.toFixed(1) || '-';
        document.getElementById('avgCS').textContent = perf.csPerMinute?.toFixed(1) || '-';
        document.getElementById('avgVision').textContent = perf.visionScore?.toFixed(1) || '-';
        document.getElementById('avgDamage').textContent = perf.damagePerMinute?.toFixed(0) || '-';

        // Update insights
        const insightsList = document.getElementById('performanceInsights');
        if (perf.insights && perf.insights.length > 0) {
            insightsList.innerHTML = perf.insights
                .map(insight => `<li><i class="fas fa-circle"></i> <span>${insight}</span></li>`)
                .join('');
        }

        // Update narrative
        document.getElementById('performanceNarrative').textContent =
            perf.narrative || 'Loading your performance analysis...';
    }

    // Populate champions section
    function populateChampions() {
        if (!reportData || !reportData.champions) return;

        const championsGrid = document.getElementById('championsGrid');
        const champions = reportData.champions.topChampions || [];

        if (champions.length === 0) {
            championsGrid.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No champion data available</p>';
            return;
        }

        championsGrid.innerHTML = champions.map((champ, index) => `
            <div class="champion-card ${index === 0 ? 'featured' : ''}">
                <div class="champion-header">
                    <div class="champion-icon">
                        <i class="fas fa-chess-knight"></i>
                    </div>
                    <div class="champion-basic-info">
                        <h3>${champ.name}</h3>
                        <div class="champion-role">${champ.role}</div>
                    </div>
                </div>

                <div class="champion-stats">
                    <div class="champion-stat">
                        <div class="stat-label">Games</div>
                        <div class="stat-value">${champ.gamesPlayed}</div>
                    </div>
                    <div class="champion-stat">
                        <div class="stat-label">Win Rate</div>
                        <div class="stat-value">${champ.winRate}%</div>
                    </div>
                    <div class="champion-stat">
                        <div class="stat-label">KDA</div>
                        <div class="stat-value">${champ.kda.toFixed(2)}</div>
                    </div>
                </div>

                <div class="champion-performance">
                    <div class="performance-metric">
                        <div class="label">CS/Min</div>
                        <div class="value">${champ.csPerMin?.toFixed(1) || '-'}</div>
                    </div>
                    <div class="performance-metric">
                        <div class="label">DMG/Min</div>
                        <div class="value">${champ.damagePerMin?.toFixed(0) || '-'}</div>
                    </div>
                    <div class="performance-metric">
                        <div class="label">Vision</div>
                        <div class="value">${champ.visionScore?.toFixed(1) || '-'}</div>
                    </div>
                </div>

                <div class="champion-description">
                    <p>${champ.description || 'Your signature champion'}</p>
                </div>
            </div>
        `).join('');

        // Update insights
        const insightsList = document.getElementById('championsInsights');
        if (reportData.champions.insights && reportData.champions.insights.length > 0) {
            insightsList.innerHTML = reportData.champions.insights
                .map(insight => `<li><i class="fas fa-circle"></i> <span>${insight}</span></li>`)
                .join('');
        }

        // Update narrative
        document.getElementById('championsNarrative').textContent =
            reportData.champions.narrative || 'Loading your champion analysis...';
    }

    // Populate team impact section
    function populateTeamImpact() {
        if (!reportData || !reportData.teamImpact) return;

        const team = reportData.teamImpact;

        // Update stats
        document.getElementById('killParticipation').textContent = `${team.killParticipation || 0}%`;
        document.getElementById('objectiveControl').textContent = `${team.objectiveControl || 0}%`;
        document.getElementById('teamfightPresence').textContent = `${team.teamfightPresence || 0}%`;
        document.getElementById('supportRating').textContent = team.supportRating?.toFixed(1) || '-';

        // Update insights
        const insightsList = document.getElementById('teamInsights');
        if (team.insights && team.insights.length > 0) {
            insightsList.innerHTML = team.insights
                .map(insight => `<li><i class="fas fa-circle"></i> <span>${insight}</span></li>`)
                .join('');
        }

        // Update narrative
        document.getElementById('teamNarrative').textContent =
            team.narrative || 'Loading your team impact analysis...';
    }

    // Populate growth section
    function populateGrowth() {
        if (!reportData || !reportData.growth) return;

        const growth = reportData.growth;

        // Update stats
        document.getElementById('kdaImprovement').textContent = `+${growth.kdaImprovement || 0}%`;
        document.getElementById('rankProgress').textContent = growth.rankProgress || '-';
        document.getElementById('championPoolGrowth').textContent = `+${growth.newChampions || 0}`;
        document.getElementById('consistencyScore').textContent = `${growth.consistency || 0}%`;

        // Update insights
        const insightsList = document.getElementById('growthInsights');
        if (growth.insights && growth.insights.length > 0) {
            insightsList.innerHTML = growth.insights
                .map(insight => `<li><i class="fas fa-circle"></i> <span>${insight}</span></li>`)
                .join('');
        }

        // Update narrative
        document.getElementById('growthNarrative').textContent =
            growth.narrative || 'Loading your growth analysis...';
    }

    // Populate achievements section
    function populateAchievements() {
        if (!reportData || !reportData.achievements) return;

        const achievementsGrid = document.getElementById('achievementsGrid');
        const achievements = reportData.achievements.list || [];

        if (achievements.length === 0) {
            achievementsGrid.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No achievements unlocked yet</p>';
            return;
        }

        achievementsGrid.innerHTML = achievements.map(achievement => `
            <div class="achievement-card ${achievement.rarity.toLowerCase()}">
                <div class="achievement-icon">
                    <i class="${achievement.icon || 'fas fa-trophy'}"></i>
                </div>
                <div class="achievement-content">
                    <h3>${achievement.name}</h3>
                    <p class="achievement-desc">${achievement.description}</p>
                    <div class="achievement-date">${achievement.date}</div>
                </div>
            </div>
        `).join('');

        // Outstanding games
        const outstandingGames = document.getElementById('outstandingGames');
        const topGames = reportData.achievements.topGames || [];

        if (topGames.length > 0) {
            outstandingGames.innerHTML = topGames.slice(0, 5).map((game, index) => `
                <div class="match-item ${game.result}">
                    <div class="match-basic-info">
                        <div class="match-result">
                            <div class="result-text">${game.result}</div>
                            <div class="match-duration">${game.duration}</div>
                        </div>
                        <div class="champion-info">
                            <div class="champion-icon">
                                <i class="fas fa-chess-knight"></i>
                            </div>
                            <div class="champion-details">
                                <div class="champion-name">${game.champion}</div>
                                <div class="role">${game.role}</div>
                            </div>
                        </div>
                    </div>
                    <div class="match-kda">
                        <span class="kda-score">${game.kills}/${game.deaths}/${game.assists}</span>
                        <span class="kda-ratio">${game.kda.toFixed(2)} KDA</span>
                    </div>
                    <div class="match-analysis">
                        <div class="performance-grade ${game.grade}">${game.grade}</div>
                    </div>
                </div>
            `).join('');
        }

        // Update narrative
        document.getElementById('achievementsNarrative').textContent =
            reportData.achievements.narrative || 'Loading your achievements...';
    }

    // Populate future goals section
    function populateFutureGoals() {
        if (!reportData || !reportData.futureGoals) return;

        const goals = reportData.futureGoals;

        // Populate each goal category
        const categories = ['mechanical', 'strategy', 'champion', 'mental', 'team'];
        categories.forEach(category => {
            const goalsList = document.getElementById(`${category}Goals`);
            const categoryGoals = goals[category] || [];

            if (categoryGoals.length > 0) {
                goalsList.innerHTML = categoryGoals.map((goal, index) => `
                    <div class="goal-card">
                        <div class="goal-header">
                            <h4>${goal.title}</h4>
                            <span class="priority-badge ${goal.priority.toLowerCase()}">${goal.priority}</span>
                        </div>
                        <p>${goal.description}</p>
                        <div class="goal-progress">
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${goal.progress || 0}%"></div>
                            </div>
                            <span>${goal.progress || 0}%</span>
                        </div>
                        <div class="action-items">
                            <h5>Action Steps:</h5>
                            ${goal.actions.map((action, i) => `
                                <div class="action-item">
                                    <input type="checkbox" id="${category}-${index}-${i}" ${action.completed ? 'checked' : ''}>
                                    <label for="${category}-${index}-${i}">${action.text}</label>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('');
            }

            // Update progress bar
            const progress = calculateCategoryProgress(categoryGoals);
            document.getElementById(`${category}Progress`).style.width = `${progress}%`;
        });

        // Update narrative
        document.getElementById('goalsNarrative').textContent =
            goals.narrative || 'These personalized goals are designed to help you improve...';
    }

    // Helper function to calculate category progress
    function calculateCategoryProgress(goals) {
        if (goals.length === 0) return 0;

        const totalProgress = goals.reduce((sum, goal) => sum + (goal.progress || 0), 0);
        return Math.round(totalProgress / goals.length);
    }

    // Download report
    async function downloadReport() {
        const authToken = localStorage.getItem('authToken');
        const summonerPuuid = localStorage.getItem('summonerPuuid');

        try {
            const response = await fetch(
                `${AWS_CONFIG.apiEndpoint}/report/${summonerPuuid}/download?format=pdf`,
                {
                    headers: {
                        'Authorization': `Bearer ${authToken}`
                    }
                }
            );

            if (!response.ok) {
                throw new Error('Failed to download report');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `summoners-chronicle-${new Date().getFullYear()}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

        } catch (error) {
            console.error('Download error:', error);
            alert('Failed to download report. Please try again.');
        }
    }

    // Share report
    function shareReport() {
        // TODO: Implement sharing functionality
        const shareData = {
            title: 'My Summoner\'s Chronicle',
            text: 'Check out my League of Legends performance insights!',
            url: window.location.href
        };

        if (navigator.share) {
            navigator.share(shareData).catch(err => console.error('Share error:', err));
        } else {
            // Fallback: copy link
            navigator.clipboard.writeText(window.location.href).then(() => {
                alert('Link copied to clipboard!');
            });
        }
    }

    // Logout
    function logout() {
        if (confirm('Are you sure you want to logout?')) {
            localStorage.clear();
            window.location.href = '../index.html';
        }
    }

    // Initialize on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDashboard);
    } else {
        initDashboard();
    }

    console.log('Dashboard module initialized');
})();
