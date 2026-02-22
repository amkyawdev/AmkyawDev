import './api/chat-api.js';
import './api/firebase.js';
import './components/nav/bar.js';
import './components/nav/button.js';
import './components/nav/aside.js';

// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyAr7Hv2ApKtNTxF11MhT5cuWeg_Dgsh0TY",
    authDomain: "smart-burme-app.firebaseapp.com",
    projectId: "smart-burme-app",
    storageBucket: "smart-burme-app.appspot.com",
    messagingSenderId: "851502425686",
    appId: "1:851502425686:web:f29e0e1dfa84794b4abdf7"
};

firebase.initializeApp(firebaseConfig);

// Three.js Space Background
class SpaceBackground {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById('canvas-container').appendChild(this.renderer.domElement);
        
        this.camera.position.z = 30;
        this.createStars();
        this.createFloatingObjects();
        this.animate();
    }

    createStars() {
        const geometry = new THREE.BufferGeometry();
        const vertices = [];
        for (let i = 0; i < 3000; i++) {
            const x = (Math.random() - 0.5) * 2000;
            const y = (Math.random() - 0.5) * 2000;
            const z = (Math.random() - 0.5) * 2000;
            vertices.push(x, y, z);
        }
        geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
        const material = new THREE.PointsMaterial({ color: 0xffffff, size: 0.5 });
        const stars = new THREE.Points(geometry, material);
        this.scene.add(stars);
        this.stars = stars;
    }

    createFloatingObjects() {
        // Create floating geometric shapes
        const colors = [0x8b5cf6, 0xec4899, 0x3b82f6, 0x10b981];
        
        for (let i = 0; i < 20; i++) {
            const geometry = new THREE.IcosahedronGeometry(Math.random() * 0.5 + 0.3, 0);
            const material = new THREE.MeshStandardMaterial({
                color: colors[Math.floor(Math.random() * colors.length)],
                emissive: 0x222222,
                roughness: 0.2,
                metalness: 0.8,
                transparent: true,
                opacity: 0.6
            });
            const mesh = new THREE.Mesh(geometry, material);
            
            mesh.position.x = (Math.random() - 0.5) * 40;
            mesh.position.y = (Math.random() - 0.5) * 40;
            mesh.position.z = (Math.random() - 0.5) * 40;
            
            mesh.userData = {
                speed: Math.random() * 0.02,
                rotationSpeed: Math.random() * 0.01
            };
            
            this.scene.add(mesh);
            this.floatingObjects = this.floatingObjects || [];
            this.floatingObjects.push(mesh);
        }
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Rotate stars
        if (this.stars) {
            this.stars.rotation.y += 0.0002;
        }
        
        // Animate floating objects
        if (this.floatingObjects) {
            this.floatingObjects.forEach(obj => {
                obj.rotation.x += obj.userData.rotationSpeed;
                obj.rotation.y += obj.userData.rotationSpeed;
                obj.position.y += Math.sin(Date.now() * obj.userData.speed) * 0.01;
            });
        }
        
        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// Loader Animation
class Loader {
    constructor() {
        this.loader = document.getElementById('loader');
        this.app = document.getElementById('app');
        this.progress = document.getElementById('loader-progress');
        this.currentProgress = 0;
    }

    start() {
        const interval = setInterval(() => {
            this.currentProgress += Math.random() * 10;
            if (this.currentProgress >= 100) {
                this.currentProgress = 100;
                this.progress.style.width = '100%';
                clearInterval(interval);
                setTimeout(() => this.hide(), 500);
            }
            this.progress.style.width = this.currentProgress + '%';
        }, 200);
    }

    hide() {
        this.loader.style.opacity = '0';
        setTimeout(() => {
            this.loader.classList.add('hidden');
            this.app.classList.remove('hidden');
            this.initializeApp();
        }, 500);
    }

    initializeApp() {
        // Initialize Three.js background
        const space = new SpaceBackground();
        window.addEventListener('resize', () => space.resize());

        // Initialize navigation
        new Navigation();
    }
}

// Navigation and UI Controller
class Navigation {
    constructor() {
        this.mobileBtn = document.getElementById('mobile-nav-btn');
        this.mobileSidebar = document.getElementById('mobile-sidebar');
        this.settingsBtn = document.getElementById('settings-btn');
        this.settingsModal = document.getElementById('settings-modal');
        this.closeSettings = document.getElementById('close-settings');
        this.langBtns = document.querySelectorAll('.lang-btn');
        this.mainContent = document.getElementById('main-content');

        this.initEventListeners();
        this.loadInitialContent();
    }

    initEventListeners() {
        // Mobile menu toggle
        if (this.mobileBtn) {
            this.mobileBtn.addEventListener('click', () => {
                this.mobileSidebar.classList.toggle('-translate-x-full');
            });
        }

        // Settings modal
        if (this.settingsBtn) {
            this.settingsBtn.addEventListener('click', () => {
                this.settingsModal.classList.remove('hidden');
                this.settingsModal.classList.add('flex');
            });
        }

        if (this.closeSettings) {
            this.closeSettings.addEventListener('click', () => {
                this.settingsModal.classList.add('hidden');
                this.settingsModal.classList.remove('flex');
            });
        }

        // Language selection
        this.langBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.langBtns.forEach(b => b.classList.remove('bg-purple-600'));
                this.langBtns.forEach(b => b.classList.add('bg-gray-700'));
                e.target.classList.remove('bg-gray-700');
                e.target.classList.add('bg-purple-600');
                
                const lang = e.target.dataset.lang;
                this.changeLanguage(lang);
            });
        });

        // Navigation links
        document.querySelectorAll('.nav-link, #mobile-sidebar a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = e.target.getAttribute('href').substring(1);
                this.loadPage(page);
                
                // Close mobile sidebar after navigation
                if (window.innerWidth < 1024) {
                    this.mobileSidebar.classList.add('-translate-x-full');
                }
            });
        });

        // Click outside to close mobile sidebar
        document.addEventListener('click', (e) => {
            if (window.innerWidth < 1024 && 
                !this.mobileSidebar.contains(e.target) && 
                !this.mobileBtn.contains(e.target) &&
                !this.mobileSidebar.classList.contains('-translate-x-full')) {
                this.mobileSidebar.classList.add('-translate-x-full');
            }
        });
    }

    async loadPage(page) {
        // Dynamic page loading
        const pages = {
            'public': 'pages/public-post.html',
            'chat': 'pages/chat.html',
            'group': 'pages/group.html',
            'docs': 'pages/docs.html',
            'about': 'pages/about.html'
        };

        if (pages[page]) {
            try {
                const response = await fetch(pages[page]);
                const html = await response.text();
                this.mainContent.innerHTML = html;
                
                // Load corresponding JavaScript
                const scripts = {
                    'public': () => import('./public/post.js'),
                    'chat': () => import('./chat/chat.js'),
                    'group': () => import('./group/group.js')
                };
                
                if (scripts[page]) {
                    scripts[page]().then(module => {
                        if (module.default) module.default.init();
                    });
                }
            } catch (error) {
                console.error('Error loading page:', error);
                this.loadPage('error');
            }
        }
    }

    changeLanguage(lang) {
        // Language change logic
        const translations = {
            'en': {
                'Public': 'Public',
                'Chat': 'Chat',
                'Group': 'Group',
                'Docs': 'Docs',
                'About': 'About'
            },
            'mm': {
                'Public': 'အများဆိုင်',
                'Chat': 'စကားပြော',
                'Group': 'အဖွဲ့',
                'Docs': 'စာရွက်စာတမ်း',
                'About': 'အကြောင်း'
            },
            'th': {
                'Public': 'สาธารณะ',
                'Chat': 'แชท',
                'Group': 'กลุ่ม',
                'Docs': 'เอกสาร',
                'About': 'เกี่ยวกับ'
            }
        };

        const texts = translations[lang] || translations['en'];
        document.querySelectorAll('[data-translate]').forEach(el => {
            const key = el.dataset.translate;
            if (texts[key]) {
                el.textContent = texts[key];
            }
        });
    }

    loadInitialContent() {
        this.loadPage('public');
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    const loader = new Loader();
    loader.start();
});
