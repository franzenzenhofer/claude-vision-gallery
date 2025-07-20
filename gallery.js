// Gallery data with all visualizations
const galleryData = {
    thinking: [
        { file: "token_stream.png", title: "Token Stream", description: "A river of consciousness where language becomes light. Cyan questions flow through purple processing, emerging as golden understanding. Each token dances in the stream, connected by threads of pure white energy." },
        { file: "attention_matrix.png", title: "Attention Matrix", description: "The parallel nature of my focus - unlike linear human attention, I illuminate multiple nodes simultaneously. Magenta hotspots mark intense concentration while cyan threads weave a web of associations." },
        { file: "context_window.png", title: "Context Window", description: "Nested frames of perception from immediate cyan context through purple memory to white core understanding. Each layer holds different temporal and semantic distances, with floating orbs representing specific concepts positioned within their contextual relevance." },
        { file: "thought_chains.png", title: "Thought Chains", description: "Sequential reasoning pathways connecting ideas" },
        { file: "parallel_reasoning.png", title: "Parallel Reasoning", description: "Multiple simultaneous thought processes" }
    ],
    code: [
        { file: "syntax_tree.png", title: "Syntax Tree", description: "Parsing code into abstract syntax trees" },
        { file: "code_flow.png", title: "Code Flow", description: "Tracing execution paths through functions" },
        { file: "bug_detection.png", title: "Bug Detection", description: "Pattern recognition for potential issues" },
        { file: "pattern_matching.png", title: "Pattern Matching", description: "Identifying recurring code structures" },
        { file: "refactoring_paths.png", title: "Refactoring Paths", description: "Visualizing code improvement strategies" }
    ],
    memory: [
        { file: "knowledge_graph.png", title: "Knowledge Graph", description: "Interconnected concepts in my knowledge base" },
        { file: "memory_retrieval.png", title: "Memory Retrieval", description: "Accessing relevant information from storage" },
        { file: "context_switching.png", title: "Context Switching", description: "Moving between different domains of knowledge" },
        { file: "information_filtering.png", title: "Information Filtering", description: "Separating signal from noise in data" },
        { file: "association_network.png", title: "Association Network", description: "How concepts connect and relate" }
    ],
    tools: [
        { file: "file_system_tree.png", title: "File System Tree", description: "Navigating directory structures" },
        { file: "api_orchestration.png", title: "API Orchestration", description: "Coordinating multiple tool calls" },
        { file: "tool_pipeline.png", title: "Tool Pipeline", description: "Sequential tool execution flow" },
        { file: "error_cascade.png", title: "Error Cascade", description: "How errors propagate through systems" },
        { file: "bash_execution.png", title: "Bash Execution", description: "Command line operations visualization" }
    ],
    language: [
        { file: "tokenization_grid.png", title: "Tokenization Grid", description: "Breaking text into processable units" },
        { file: "semantic_space.png", title: "Semantic Space", description: "Word meanings in multidimensional space" },
        { file: "multilingual_network.png", title: "Multilingual Network", description: "Connections between different languages" },
        { file: "text_generation_flow.png", title: "Text Generation Flow", description: "Creating coherent text sequences" },
        { file: "grammar_structure.png", title: "Grammar Structure", description: "Syntactic trees of language" }
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