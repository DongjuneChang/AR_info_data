/**
 * PositionControl class for controlling position values with a slider
 */
class PositionControl {
    /**
     * Constructor
     * @param {Object} options - Options for the position control
     * @param {number} options.min - Minimum value
     * @param {number} options.max - Maximum value
     * @param {number} options.value - Initial value
     * @param {number} options.step - Step size
     */
    constructor(options = {}) {
        this.min = options.min !== undefined ? options.min : 0.1;
        this.max = options.max !== undefined ? options.max : 3.0;
        this.value = options.value !== undefined ? options.value : 0.3;
        this.step = options.step !== undefined ? options.step : 0.1;
        
        this.element = this.createPositionControl();
        this.updatePositionValue();
        
        return this;
    }
    
    /**
     * Create the position control element
     * @returns {HTMLElement} - Position control element
     */
    createPositionControl() {
        const container = document.createElement('div');
        container.className = 'position-control';
        
        // Value display
        const valueDisplay = document.createElement('div');
        valueDisplay.className = 'position-value';
        valueDisplay.textContent = this.formatValue(this.value);
        container.appendChild(valueDisplay);
        
        // Slider
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.className = 'position-slider';
        slider.min = this.min;
        slider.max = this.max;
        slider.step = this.step;
        slider.value = this.value;
        slider.addEventListener('input', (e) => this.handleSliderInput(e));
        container.appendChild(slider);
        
        // Min/Max labels
        const labels = document.createElement('div');
        labels.className = 'position-label';
        
        const minLabel = document.createElement('span');
        minLabel.textContent = `${this.min}m`;
        labels.appendChild(minLabel);
        
        const maxLabel = document.createElement('span');
        maxLabel.textContent = `${this.max}m`;
        labels.appendChild(maxLabel);
        
        container.appendChild(labels);
        
        // Direct input
        const input = document.createElement('input');
        input.type = 'number';
        input.className = 'position-input';
        input.min = this.min;
        input.max = this.max;
        input.step = this.step;
        input.value = this.value;
        input.addEventListener('input', (e) => this.handleDirectInput(e));
        input.addEventListener('blur', (e) => this.validateInput(e));
        container.appendChild(input);
        
        return container;
    }
    
    /**
     * Handle slider input
     * @param {Event} event - Input event
     */
    handleSliderInput(event) {
        const value = parseFloat(event.target.value);
        this.setValue(value);
    }
    
    /**
     * Handle direct input
     * @param {Event} event - Input event
     */
    handleDirectInput(event) {
        const value = parseFloat(event.target.value);
        if (!isNaN(value) && value >= this.min && value <= this.max) {
            this.setValue(value);
        }
    }
    
    /**
     * Validate input on blur
     * @param {Event} event - Blur event
     */
    validateInput(event) {
        const input = event.target;
        let value = parseFloat(input.value);
        
        if (isNaN(value)) {
            value = this.value;
        } else {
            if (value < this.min) value = this.min;
            if (value > this.max) value = this.max;
        }
        
        this.setValue(value);
        input.value = value;
    }
    
    /**
     * Update the position value display
     */
    updatePositionValue() {
        const valueDisplay = this.element.querySelector('.position-value');
        valueDisplay.textContent = this.formatValue(this.value);
        
        const slider = this.element.querySelector('.position-slider');
        slider.value = this.value;
        
        const input = this.element.querySelector('.position-input');
        input.value = this.value;
    }
    
    /**
     * Format a value for display
     * @param {number} value - Value to format
     * @returns {string} - Formatted value
     */
    formatValue(value) {
        const numValue = parseFloat(value) || 0;
        return `${numValue.toFixed(2)}m`;
    }
    
    /**
     * Get the current value
     * @returns {number} - Current value
     */
    getValue() {
        return this.value;
    }
    
    /**
     * Set the value
     * @param {number} value - Value to set
     */
    setValue(value) {
        if (value >= this.min && value <= this.max) {
            this.value = value;
            this.updatePositionValue();
        }
    }
}
