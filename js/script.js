/**
 * JERUSALEM SIGNET - MASTER JAVASCRIPT
 * ---------------------------------------------------------
 * This script handles:
 * 1. Interactive Pricing (Real-time calculation $149 - $794)
 * 2. Scroll Reveal Animations (High-end fade-in effects)
 * 3. Smooth Anchor Navigation
 * ---------------------------------------------------------
 */

document.addEventListener("DOMContentLoaded", function() {
    
    // ==========================================
    // 1. PRICING ENGINE LOGIC
    // ==========================================
    const pricingInputs = document.querySelectorAll('.bespoke-builder input, .bespoke-builder select');
    const grandTotalDisplay = document.getElementById('grand-total');

    /**
     * Calculation Logic:
     * - Foundation: Gallery ($149) or Heritage ($348)
     * - Script: Custom Verse adds $99
     * - Medium: Kosher Ink adds $99
     * - Presentation: Exhibition Chest adds $149
     * - Engraving: Lid Dedication adds $99
     */
    function calculateTotal() {
        let total = 0;

        // Step 1: Foundation (Gallery $149 or Heritage $348)
        const foundation = document.querySelector('input[name="foundation"]:checked');
        if (foundation) {
            total += parseInt(foundation.value);
        }

        // Step 2: Script (Sacred Collection $0 or Custom $99)
        const script = document.getElementById('script-select');
        if (script) {
            total += parseInt(script.value);
        }

        // Step 3: Medium (Pencil $0 or Kosher Ink $99)
        const medium = document.querySelector('input[name="medium"]:checked');
        if (medium) {
            total += parseInt(medium.value);
        }

        // Step 4: Presentation (Standard $0 or Wood Chest $149)
        const presentation = document.querySelector('input[name="presentation"]:checked');
        if (presentation) {
            total += parseInt(presentation.value);
        }

        // Step 5: Bespoke Engraving (Checkbox $99)
        const engraving = document.getElementById('engraving-check');
        if (engraving && engraving.checked) {
            total += parseInt(engraving.value);
        }

        // Update the total display in the UI
        if (grandTotalDisplay) {
            grandTotalDisplay.innerText = '$' + total;
        }
    }

    // Attach listeners to all radio buttons, selects, and checkboxes
    pricingInputs.forEach(input => {
        input.addEventListener('change', calculateTotal);
    });

    // Run once on initial load to set the base price ($149)
    calculateTotal();


    // ==========================================
    // 2. SCROLL REVEAL ANIMATIONS
    // ==========================================
    
    // Targets: Gallery items, Pricing steps, and Footer branding
    const animateElements = document.querySelectorAll('.gallery-item, .step-box, .builder-summary, .product-set, .footer-branding');

    // Initial Styles: Hide elements and offset them slightly
    animateElements.forEach(el => {
        el.style.opacity = "0";
        el.style.transform = "translateY(40px)";
        el.style.transition = "all 0.9s cubic-bezier(0.2, 0.6, 0.3, 1)";
    });

    /**
     * Checks vertical scroll position to trigger reveal
     */
    function handleReveal() {
        const windowHeight = window.innerHeight;
        
        animateElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;
            const revealPoint = 100; // Trigger 100px before the element enters view

            if (elementTop < windowHeight - revealPoint) {
                el.style.opacity = "1";
                el.style.transform = "translateY(0)";
            }
        });
    }

    // Event listeners for scrolling and resizing
    window.addEventListener('scroll', handleReveal);
    window.addEventListener('resize', handleReveal);
    
    // Trigger once on load to reveal anything already in the viewport
    handleReveal();


    // ==========================================
    // 3. SMOOTH ANCHOR NAVIGATION
    // ==========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetID = this.getAttribute('href');
            const targetElement = document.querySelector(targetID);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

});