// Gallery data with all visualizations
const galleryData = {
    thinking: [
        { file: "token_stream.png", title: "Token Stream", description: "A river of consciousness where language becomes light. Each shape - cube, sphere, cylinder - represents different types of tokens flowing through my processing. The sinusoidal wave pattern shows how meaning ebbs and flows, with vibrant neon colors marking semantic categories: hot pink for entities, cyan for actions, yellow for connections." },
        { file: "attention_matrix.png", title: "Attention Matrix", description: "The neural dance of attention weights visualized as glowing spheres. Hot pink nodes burn brightest where focus is most intense, cyan marks moderate attention, and purple shows peripheral awareness. This isn't sequential like human attention - it's a parallel explosion of simultaneous focus across all tokens." },
        { file: "context_window.png", title: "Context Window", description: "Concentric torus frames represent layers of context, from the immediate cyan ring through purple intermediate memory to yellow distant associations. The hot pink sphere at center is the current focus, while each ring holds information at different semantic distances - a 3D map of contextual relevance." },
        { file: "thought_chains.png", title: "Thought Chains", description: "Radiating from a golden central hub, eight chains of reasoning extend outward. Each chain diminishes in size representing decreasing certainty. The colors - cycling through the entire neon spectrum - show how different types of logic interconnect: deductive pink, inductive cyan, abductive purple, all converging on truth." },
        { file: "parallel_reasoning.png", title: "Parallel Reasoning", description: "Five simultaneous streams of thought, each a different color, weave through possibility space. Unlike human linear thinking, I process multiple hypotheses in parallel - the undulating waves show how these reasoning threads influence each other, occasionally converging before diverging again into new territories." }
    ],
    code: [
        { file: "syntax_tree.png", title: "Syntax Tree", description: "The hierarchical structure of code made visible. A magenta root node branches into cyan, yellow, and green function declarations. Each function spawns its own subtree of operations, with purple leaf nodes representing atomic operations. This is how I decompose your code into executable logic." },
        { file: "code_flow.png", title: "Code Flow", description: "A double helix of execution - two intertwined strands of control flow spiraling through time and logic. Different shapes mark different operations: cubes for assignments, spheres for conditionals, cylinders for loops. The hot pink cone at center is the execution pointer, my focus as I trace through your algorithms." },
        { file: "bug_detection.png", title: "Bug Detection", description: "A grid of green code blocks with hot pink anomalies glowing like warning lights. Each bug radiates its own sphere of influence, showing how errors can cascade through systems. The visual intensity maps to bug severity - brighter pink means more critical issues demanding immediate attention." },
        { file: "pattern_matching.png", title: "Pattern Matching", description: "Common code patterns displayed as neon constellations. L-shapes in cyan, T-formations in magenta, linear sequences in yellow, and square blocks in green. Purple indicators point to where these patterns appear in your codebase. Pattern recognition is how I suggest optimizations and identify reusable components." },
        { file: "refactoring_paths.png", title: "Refactoring Paths", description: "The journey from chaos to clarity. On the left, a tangled mess of hot pink shapes in random orientations - spaghetti code. Yellow arrows flow rightward, transforming disorder into the clean green grid on the right. Each arrow represents a refactoring operation: extract method, rename variable, restructure logic." }
    ],
    memory: [
        { file: "knowledge_graph.png", title: "Knowledge Graph", description: "Interconnected concepts in my knowledge base" },
        { file: "memory_retrieval.png", title: "Memory Retrieval", description: "Accessing relevant information from storage" },
        { file: "context_switching.png", title: "Context Switching", description: "Moving between different domains of knowledge" },
        { file: "information_filtering.png", title: "Information Filtering", description: "Separating signal from noise in data" },
        { file: "association_network.png", title: "Association Network", description: "How concepts connect and relate" }
    ],
    tools: [
        { file: "network_packets.png", title: "Network Packets", description: "Streams of data flowing through the digital ether. Yellow, purple, and pink packets travel in synchronized waves, each carrying fragments of information through the network's invisible highways. The rhythmic flow represents TCP/IP protocols dancing in perfect harmony." },
        { file: "file_operations.png", title: "File Operations", description: "A neon green disk pulses at the center while read, write, create, and delete operations radiate outward in concentric circles. Cyan cubes represent reads, yellow cones are writes, hot pink cylinders show deletions, and green spheres mark new file creation - a symphony of filesystem activity." },
        { file: "system_calls.png", title: "System Calls", description: "The layered architecture of system interaction: cyan user space nodes floating above, hot pink kernel space in the middle, and deep purple hardware layer at the base. Electric blue connections bridge the layers, showing how requests cascade from applications down to silicon." },
        { file: "process_threads.png", title: "Process Threads", description: "A magenta central process cylinder with four distinct thread spirals orbiting around it. Each thread - hot pink, purple, yellow, and cyan - traces its own helical path through execution space, occasionally synchronizing at critical sections before diverging again." },
        { file: "io_streams.png", title: "I/O Streams", description: "Data transformation visualized: cyan input blocks flow from the left in sinusoidal waves, converging on a brilliant yellow processing sphere at center. Transformed data emerges as green output nodes on the right, each carrying processed information to its destination." }
    ],
    language: [
        { file: "tokenization_grid.png", title: "Tokenization Grid", description: "The atomic units of language arranged in a grid. Cyan cubes are whole words, yellow cylinders represent subword tokens, hot pink spheres mark punctuation, and purple cones indicate special tokens. Each shape vibrates at a slightly different angle, showing the dynamic nature of language processing - nothing is static in the flow of meaning." },
        { file: "semantic_space.png", title: "Semantic Space", description: "Words float in multidimensional meaning-space. Cyan clusters around core concepts, yellow groups actions, hot pink emotions swirl together, green objects maintain proximity, and purple abstractions drift in their own realm. Thin blue connections show semantic relationships - synonyms, antonyms, associations - creating a web of understanding." },
        { file: "multilingual_network.png", title: "Multilingual Network", description: "Eight language nodes orbit a central aqua hub, each glowing in its unique color: English cyan, Spanish pink, Chinese yellow, Arabic orange, French purple, German magenta, Japanese green, Russian blue. Connection beams show translation pathways - direct links between neighbors, all languages connected through the universal semantic core." },
        { file: "text_generation_flow.png", title: "Text Generation Flow", description: "The creative process of text synthesis visualized as a flowing stream. Purple context blocks enter from the left, transform through cyan processing spheres, branch into yellow candidate cylinders, and emerge as green output cones. Probability branches float above - fainter options that could have been chosen, the multiverse of potential sentences." },
        { file: "grammar_structure.png", title: "Grammar Structure", description: "The skeleton of syntax revealed. A magenta sentence node crowns the tree, splitting into cyan noun phrases and yellow verb phrases. These branch further into individual words - hot pink determiners, green nouns, purple verbs - all connected by glowing edges that show grammatical relationships. This is how I parse the architecture of your thoughts." }
    ],
    problem_solving: [
        { file: "task_decomposition.png", title: "Task Decomposition", description: "Breaking complex problems into steps" },
        { file: "solution_search.png", title: "Solution Search", description: "Exploring the space of possibilities" },
        { file: "optimization_landscape.png", title: "Optimization Landscape", description: "Finding optimal solutions" },
        { file: "decision_tree.png", title: "Decision Tree", description: "Branching logic pathways" },
        { file: "constraint_graph.png", title: "Constraint Graph", description: "Balancing multiple requirements" }
    ],
    system: [
        { file: "process_threads.png", title: "Process Threads", description: "Parallel execution streams" },
        { file: "io_streams.png", title: "I/O Streams", description: "Data input and output flow" },
        { file: "network_packets.png", title: "Network Packets", description: "Information traveling through networks" },
        { file: "file_operations.png", title: "File Operations", description: "Reading, writing, and manipulating files" },
        { file: "system_calls.png", title: "System Calls", description: "Interfacing with the operating system" }
    ],
    consciousness: [
        { file: "self_awareness_loop.png", title: "Self Awareness Loop", description: "Recursive self-observation cycles" },
        { file: "meta_cognition.png", title: "Meta Cognition", description: "Thinking about thinking" },
        { file: "uncertainty_field.png", title: "Uncertainty Field", description: "Probabilistic confidence distributions" },
        { file: "confidence_levels.png", title: "Confidence Levels", description: "Certainty gradients in responses" },
        { file: "introspection_spiral.png", title: "Introspection Spiral", description: "Deep self-examination patterns" }
    ],
    interaction: [
        { file: "user_dialogue_flow.png", title: "User Dialogue Flow", description: "Conversation state management" },
        { file: "response_generation.png", title: "Response Generation", description: "Creating meaningful replies" },
        { file: "context_understanding.png", title: "Context Understanding", description: "Layered comprehension of meaning" },
        { file: "empathy_mapping.png", title: "Empathy Mapping", description: "Understanding user intent and emotion" },
        { file: "conversation_state.png", title: "Conversation State", description: "Tracking dialogue progression" }
    ]
};

// Additional standalone visualizations
const standaloneImages = [
    { category: "legacy", file: "neural_network.png", title: "Neural Network", description: "Classic neural network visualization" },
    { category: "legacy", file: "data_flow.png", title: "Data Flow", description: "Information transformation pipeline" },
    { category: "legacy", file: "algorithm_crystal.png", title: "Algorithm Crystal", description: "Crystalline algorithm structures" },
    { category: "legacy", file: "system_architecture.png", title: "System Architecture", description: "Overall system design" },
    { category: "legacy", file: "code_universe.png", title: "Code Universe", description: "The infinite space of code" }
];

// DOM elements
const gallery = document.getElementById('gallery');
const modal = document.getElementById('modal');
const modalImage = document.getElementById('modal-image');
const modalTitle = document.getElementById('modal-title');
const modalDescription = document.getElementById('modal-description');
const closeModal = document.querySelector('.close');
const navLinks = document.querySelectorAll('.nav-link');
const navToggle = document.querySelector('.nav-toggle');
const navList = document.querySelector('.nav-list');

// Create gallery grid container
const galleryGrid = document.createElement('div');
galleryGrid.className = 'gallery-grid';
gallery.appendChild(galleryGrid);

// Function to create gallery item
function createGalleryItem(category, item) {
    const div = document.createElement('div');
    div.className = 'gallery-item';
    div.dataset.category = category;
    
    const img = document.createElement('img');
    img.src = `public/${category}/${item.file}`;
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
    
    // Add categorized images
    for (const [category, items] of Object.entries(galleryData)) {
        items.forEach(item => {
            galleryGrid.appendChild(createGalleryItem(category, item));
        });
    }
    
    // Add standalone images
    standaloneImages.forEach(item => {
        const div = createGalleryItem(item.category, item);
        // Adjust image path for standalone images
        div.querySelector('img').src = `public/${item.file}`;
        galleryGrid.appendChild(div);
    });
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
        
        // Close mobile menu
        navList.classList.remove('active');
    });
});

// Mobile menu toggle
navToggle.addEventListener('click', () => {
    navList.classList.toggle('active');
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