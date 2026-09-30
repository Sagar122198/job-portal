// ============================================================================
// JOB SEARCH FUNCTIONALITY
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    const searchbar = document.querySelector('.js-jobSearchbar')
    const jobTitle = document.querySelectorAll('.js-jobTitle')

    if (!searchbar || !jobTitle.length) {
        return
    }

    searchbar.addEventListener('input', (e) => {
        const value = e.target.value.toLowerCase().trim()
        jobTitle.forEach((titles) => {
            const card = titles.closest('[data-job-card]')
            if (titles.innerText.toLowerCase().includes(value)) {
                card.style.display = ''  // Reset to CSS default (grid)
            } else {
                card.style.display = 'none'
            }
        })
    })
})

// ============================================================================
// MOBILE NAVIGATION MENU TOGGLE
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.querySelector('[data-mobile-menu-btn]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    const iconOpen = document.querySelector('[data-menu-icon-open]');
    const iconClose = document.querySelector('[data-menu-icon-close]');

    if (!menuBtn || !mobileMenu) return;

    menuBtn.addEventListener('click', () => {
        const isOpen = !mobileMenu.classList.contains('hidden');
        mobileMenu.classList.toggle('hidden');
        if (iconOpen) iconOpen.classList.toggle('hidden');
        if (iconClose) iconClose.classList.toggle('hidden');
        menuBtn.setAttribute('aria-expanded', !isOpen);
    });
});

// ============================================================================
// SAVE JOB — HEART TOGGLE ANIMATION
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-save-btn]').forEach(btn => {
        btn.addEventListener('click', () => {
            const heart = btn.querySelector('.jc__heart');
            const isSaved = btn.classList.toggle('is-saved');
            heart.textContent = isSaved ? '♥' : '♡';
            // Re-trigger animation
            heart.style.animation = 'none';
            heart.offsetHeight; // force reflow
            heart.style.animation = '';
        });
    });
});

// ============================================================================
// SHARE JOB — COPY TO CLIPBOARD WITH TOOLTIP
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-share-btn]').forEach(btn => {
        btn.addEventListener('click', () => {
            const path = btn.getAttribute('data-url');
            const fullUrl = window.location.origin + path;
            const tooltip = btn.querySelector('.jc__tooltip');

            navigator.clipboard.writeText(fullUrl).then(() => {
                if (tooltip) {
                    tooltip.textContent = 'Copied!';
                    tooltip.classList.add('is-visible');
                    setTimeout(() => {
                        tooltip.classList.remove('is-visible');
                    }, 1800);
                }
            }).catch(() => {
                // Fallback for older browsers
                const ta = document.createElement('textarea');
                ta.value = fullUrl;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                if (tooltip) {
                    tooltip.textContent = 'Copied!';
                    tooltip.classList.add('is-visible');
                    setTimeout(() => tooltip.classList.remove('is-visible'), 1800);
                }
            });
        });
    });
});

// ============================================================================
// MORE OPTIONS DROPDOWN
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-more-btn]').forEach(btn => {
        const dropdown = btn.closest('.jc__more-wrap')?.querySelector('[data-more-dropdown]');
        if (!dropdown) return;

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            // Close all other dropdowns first
            document.querySelectorAll('[data-more-dropdown].is-open').forEach(d => {
                if (d !== dropdown) d.classList.remove('is-open');
            });
            dropdown.classList.toggle('is-open');
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        document.querySelectorAll('[data-more-dropdown].is-open').forEach(d => {
            d.classList.remove('is-open');
        });
    });
});

// ============================================================================
// SKILL CHIP OVERFLOW — Show +N for hidden chips
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-skills-container]').forEach(container => {
        const maxChips = parseInt(container.getAttribute('data-max-chips')) || 999;
        const skills = container.querySelectorAll('[data-skill]');
        let hiddenCount = 0;

        skills.forEach((skill, index) => {
            if (index >= maxChips) {
                skill.style.display = 'none';
                hiddenCount++;
            }
        });

        if (hiddenCount > 0) {
            const isSmall = container.closest('.jc-sm');
            const moreChip = document.createElement('span');
            moreChip.className = isSmall
                ? 'jc-sm__skill jc-sm__skill--more'
                : 'jc__skill jc__skill--more';
            moreChip.textContent = `+${hiddenCount}`;
            container.appendChild(moreChip);
        }
    });
});

// ============================================================================
// APPLICANT MANAGEMENT - DRAWER
// ============================================================================
function openApplicantsDrawer(jobId) {
    const drawer = document.getElementById('applicantsDrawer');
    const overlay = document.getElementById('applicantsOverlay');
    const content = document.getElementById('applicantsContent');
    
    overlay.classList.remove('hidden');
    drawer.classList.remove('translate-x-full');
    
    // Fetch applicants
    fetch(`/job/${jobId}/applicants/`)
        .then(response => response.json())
        .then(data => {
            if (data.applicants && data.applicants.length > 0) {
                let html = '<ul class="space-y-3">';
                data.applicants.forEach(applicant => {
                    const statusColors = {
                        'pending': 'bg-yellow-50 text-yellow-700 border-yellow-200',
                        'shortlisted': 'bg-green-50 text-green-700 border-green-200',
                        'rejected': 'bg-red-50 text-red-700 border-red-200',
                        'submitted': 'bg-blue-50 text-blue-700 border-blue-200'
                    };
                    const colors = statusColors[applicant.status] || statusColors['submitted'];
                    
                    html += `
                        <li class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition cursor-pointer" 
                            onclick="viewApplicantDetail(${jobId}, ${applicant.id})">
                            <div class="flex items-start justify-between">
                                <div class="flex-1">
                                    <p class="font-semibold text-gray-900">${applicant.applicant_name}</p>
                                    <p class="text-sm text-gray-600">${applicant.applicant_email}</p>
                                    <p class="text-xs text-gray-500 mt-1">
                                        Submitted: ${new Date(applicant.submitted_at).toLocaleDateString()}
                                    </p>
                                </div>
                                <span class="ml-2 px-3 py-1 rounded-full text-xs font-semibold border ${colors}">
                                    ${applicant.status}
                                </span>
                            </div>
                        </li>
                    `;
                });
                html += '</ul>';
                content.innerHTML = html;
            } else {
                content.innerHTML = '<p class="text-center text-gray-500">No applicants yet.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            content.innerHTML = '<p class="text-center text-red-500">Error loading applicants</p>';
        });
}

function closeApplicantsDrawer() {
    const drawer = document.getElementById('applicantsDrawer');
    const overlay = document.getElementById('applicantsOverlay');
    
    drawer.classList.add('translate-x-full');
    overlay.classList.add('hidden');
}

function viewApplicantDetail(jobId, applicationId) {
    window.location.href = `/job/${jobId}/applicant/${applicationId}/`;
}

// Close drawer on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeApplicantsDrawer();
    }
});

// ============================================================================
// APPLICANT DETAIL - STATUS UPDATE
// ============================================================================
function updateStatus(applicationId, newStatus) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                      document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
    
    const formData = new FormData();
    formData.append('status', newStatus);
    
    fetch(`/applicant/${applicationId}/status/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error: ' + (data.error || 'Failed to update status'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred');
    });
}

// ============================================================================
// JOB APPLICATIONS DASHBOARD - TOGGLE & REAL-TIME UPDATES
// ============================================================================
function toggleApplications(button) {
    const container = button.closest('[data-job-applications-dashboard]');
    const applicationsDiv = container.querySelector('[data-applications-container]');
    const arrow = button.querySelector('[data-arrow-icon]');
    
    applicationsDiv.classList.toggle('hidden');
    if (arrow) {
        arrow.classList.toggle('rotate-90');
    }
}

// Real-time job applications dashboard for job seekers
document.addEventListener('DOMContentLoaded', function() {
    const dashboardContainer = document.querySelector('[data-job-applications-dashboard]');
    
    if (!dashboardContainer) return; // Only run if dashboard exists
    
    // Fetch and update applications every 30 seconds
    const updateApplications = async () => {
        try {
            const response = await fetch('/job/api/my-applications/');
            if (!response.ok) return;
            
            const data = await response.json();
            
            // Update badge count
            const badge = dashboardContainer?.querySelector('[role="status"]');
            if (badge && data.count !== undefined) {
                badge.textContent = `${data.count} applications`;
            }
            
            // Update each application's status dynamically
            if (data.applications) {
                data.applications.forEach(app => {
                    const appElement = document.querySelector(`[data-app-id="${app.id}"]`);
                    if (appElement) {
                        const statusBadge = appElement.querySelector('[data-status]');
                        if (statusBadge && statusBadge.getAttribute('data-status') !== app.status) {
                            // Update status badge with appropriate color
                            const newClass = {
                                'shortlisted': 'bg-green-100 text-green-800',
                                'rejected': 'bg-red-100 text-red-800',
                                'pending': 'bg-yellow-100 text-yellow-800',
                                'submitted': 'bg-blue-100 text-blue-800'
                            }[app.status] || 'bg-blue-100 text-blue-800';
                            
                            statusBadge.className = `inline-block px-2.5 py-1 rounded-full text-xs font-semibold ${newClass}`;
                            statusBadge.textContent = app.status_display;
                            statusBadge.setAttribute('data-status', app.status);
                            
                            // Add a subtle pulse animation to show the change
                            appElement.classList.add('animate-pulse');
                            setTimeout(() => appElement.classList.remove('animate-pulse'), 1000);
                        }
                    }
                });
            }
        } catch (error) {
            console.error('Error updating applications:', error);
        }
    };
    
    // Update immediately and then every 30 seconds
    updateApplications();
    setInterval(updateApplications, 30000);
});

// ============================================================================
// DELETE MODAL HANDLERS
// ============================================================================
function openDeleteModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
}

function closeDeleteModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}
