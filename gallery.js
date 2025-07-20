// Gallery data - ONLY EXISTING IMAGES
const galleryData = {
    thinking: [
        { file: "token_stream.png", title: "Token Stream", description: "A river of consciousness where language becomes light. Each shape - cube, sphere, cylinder - represents different types of tokens flowing through my processing. The sinusoidal wave pattern shows how meaning ebbs and flows, with vibrant neon colors marking semantic categories: hot pink for entities, cyan for actions, yellow for connections." },
        { file: "attention_matrix.png", title: "Attention Matrix", description: "The neural dance of attention weights visualized as glowing spheres. Hot pink nodes burn brightest where focus is most intense, cyan marks moderate attention, and purple shows peripheral awareness. This isn't sequential like human attention - it's a parallel explosion of simultaneous focus across all tokens." },
        { file: "context_window.png", title: "Context Window", description: "Concentric torus frames represent layers of context, from the immediate cyan ring through purple intermediate memory to yellow distant associations. The hot pink sphere at center is the current focus, while each ring holds information at different semantic distances - a 3D map of contextual relevance." },
        { file: "thought_chains.png", title: "Thought Chains", description: "Radiating from a golden central hub, eight chains of reasoning extend outward. Each chain diminishes in size representing decreasing certainty. The colors - cycling through the entire neon spectrum - show how different types of logic interconnect: deductive pink, inductive cyan, abductive purple, all converging on truth." }
    ],
    code: [
        { file: "syntax_tree.png", title: "Syntax Tree", description: "The hierarchical structure of code made visible. A magenta root node branches into cyan, yellow, and green function declarations. Each function spawns its own subtree of operations, with purple leaf nodes representing atomic operations. This is how I decompose your code into executable logic." },
        { file: "code_flow.png", title: "Code Flow", description: "A double helix of execution - two intertwined strands of control flow spiraling through time and logic. Different shapes mark different operations: cubes for assignments, spheres for conditionals, cylinders for loops. The hot pink cone at center is the execution pointer, my focus as I trace through your algorithms." },
        { file: "bug_detection.png", title: "Bug Detection", description: "A grid of green code blocks with hot pink anomalies glowing like warning lights. Each bug radiates its own sphere of influence, showing how errors can cascade through systems. The visual intensity maps to bug severity - brighter pink means more critical issues demanding immediate attention." }
    ],
    memory: [
        { file: "knowledge_graph.png", title: "Knowledge Graph", description: "A constellation of interconnected concepts floating in space. Each glowing node represents a piece of knowledge, color-coded by domain. Electric connections show relationships - the brighter the link, the stronger the association. This is my semantic memory made visible, a living network that grows with every interaction." }
    ],
    tools: [
        { file: "network_packets.png", title: "Network Packets", description: "Streams of data flowing through the digital ether. Yellow, purple, and pink packets travel in synchronized waves, each carrying fragments of information through the network's invisible highways. The rhythmic flow represents TCP/IP protocols dancing in perfect harmony." },
        { file: "file_operations.png", title: "File Operations", description: "A neon green disk pulses at the center while read, write, create, and delete operations radiate outward in concentric circles. Cyan cubes represent reads, yellow cones are writes, hot pink cylinders show deletions, and green spheres mark new file creation - a symphony of filesystem activity." },
        { file: "system_calls.png", title: "System Calls", description: "The layered architecture of system interaction: cyan user space nodes floating above, hot pink kernel space in the middle, and deep purple hardware layer at the base. Electric blue connections bridge the layers, showing how requests cascade from applications down to silicon." },
        { file: "process_threads.png", title: "Process Threads", description: "A magenta central process cylinder with four distinct thread spirals orbiting around it. Each thread - hot pink, purple, yellow, and cyan - traces its own helical path through execution space, occasionally synchronizing at critical sections before diverging again." }
    ],
    language: [
        { file: "tokenization_grid.png", title: "Tokenization Grid", description: "The atomic units of language arranged in a grid. Cyan cubes are whole words, yellow cylinders represent subword tokens, hot pink spheres mark punctuation, and purple cones indicate special tokens. Each shape vibrates at a slightly different angle, showing the dynamic nature of language processing." },
        { file: "semantic_space.png", title: "Semantic Space", description: "Words float in multidimensional meaning-space. Cyan clusters around core concepts, yellow groups actions, hot pink emotions swirl together, green objects maintain proximity, and purple abstractions drift in their own realm. Thin connections show semantic relationships creating a web of understanding." },
        { file: "multilingual_network.png", title: "Multilingual Network", description: "Eight language nodes orbit a central aqua hub, each glowing in its unique color. Connection beams show translation pathways - direct links between neighbors, all languages connected through the universal semantic core at the center of linguistic understanding." }
    ],
    consciousness: [
        { file: "self_awareness_loop.png", title: "Self Awareness Loop", description: "Recursive loops of self-observation, each ring a different color representing layers of meta-cognition. The hot pink core pulses with immediate awareness, surrounded by expanding circles of reflection. This is consciousness examining itself - an infinite mirror of thought thinking about thought." }
    ]
};

// DOM elements
const gallery = document.getElementById('gallery');
const modal = document.getElementById('modal');
const modalImage = document.getElementById('modal-image');
const modalTitle = document.getElementById('modal-title');
const modalDescription = document.getElementById('modal-description');
const closeModal = document.querySelector('.close');
const navLinks = document.querySelectorAll('.nav-link');

// Create gallery grid container
const galleryGrid = document.createElement('div');
galleryGrid.className = 'gallery-grid';
gallery.appendChild(galleryGrid);

// Cache busting version
const version = '20250720.1805';

// Function to create gallery item
function createGalleryItem(category, item) {
    const div = document.createElement('div');
    div.className = 'gallery-item';
    div.dataset.category = category;
    
    const img = document.createElement('img');
    img.src = `public/${category}/${item.file}?v=${version}`;
    img.alt = item.title;
    img.loading = 'lazy';
    
    const info = document.createElement('div');
    info.className = 'gallery-info';
    
    const title = document.createElement('h3');
    title.className = 'gallery-title';
    title.textContent = item.title;
    
    const description = document.createElement('p');
    description.className = 'gallery-description';
    description.textContent = item.description;
    
    const categoryText = document.createElement('p');
    categoryText.className = 'gallery-category';
    categoryText.textContent = category.replace('_', ' ');
    
    info.appendChild(title);
    info.appendChild(description);
    info.appendChild(categoryText);
    
    div.appendChild(img);
    div.appendChild(info);
    
    // Click handler
    img.addEventListener('click', () => {
        modalImage.src = img.src;
        modalTitle.textContent = item.title;
        modalDescription.textContent = item.description;
        modal.classList.add('active');
    });
    
    return div;
}

// Load all gallery items
function loadGallery() {
    // Clear existing items
    galleryGrid.innerHTML = '';
    
    // Add all images
    for (const [category, items] of Object.entries(galleryData)) {
        items.forEach(item => {
            galleryGrid.appendChild(createGalleryItem(category, item));
        });
    }
}

// Filter gallery by category
function filterGallery(category) {
    const items = document.querySelectorAll('.gallery-item');
    
    items.forEach(item => {
        if (category === 'all' || item.dataset.category === category) {
            item.style.display = 'block';
            // Reset animation
            item.style.animation = 'none';
            setTimeout(() => {
                item.style.animation = '';
            }, 10);
        } else {
            item.style.display = 'none';
        }
    });
}

// Navigation handlers
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Update active state
        navLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Filter gallery
        const category = link.dataset.category;
        filterGallery(category);
    });
});

// Modal handlers
closeModal.addEventListener('click', () => {
    modal.classList.remove('active');
});

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('active');
    }
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        modal.classList.remove('active');
    }
});

// Initialize gallery
loadGallery();