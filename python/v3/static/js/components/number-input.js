/**
 * NumberInput class for numeric input with validation and step buttons
 */
class NumberInput {
    /**
     * Constructor
     * @param {Object} schema - Schema for the number input
     */
    constructor(schema) {
        this.schema = schema || {};
        this.value = parseFloat(schema.default) || 0;
        this.lastValidValue = this.value;
        
        const container = this.createInput();
        this.container = container;  // Store reference to container
        return container;
    }

    /**
     * Create the number input element
     * @returns {HTMLElement} - Number input element
     */
    createInput() {
        const container = document.createElement('div');
        container.className = 'number-input-container';

        // Text input for direct value input
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'number-input';
        input.value = this.schema.default || '';
        
        if (this.schema.minimum !== undefined) input.setAttribute('min', this.schema.minimum);
        if (this.schema.maximum !== undefined) input.setAttribute('max', this.schema.maximum);

        // Add event listeners
        input.addEventListener('input', (e) => this.handleInput(e));
        input.addEventListener('blur', (e) => this.handleBlur(e));
        input.addEventListener('keydown', (e) => this.handleKeyDown(e));

        // Add step buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'number-input-buttons';

        const upButton = document.createElement('button');
        upButton.textContent = '▲';
        upButton.className = 'number-input-button up';
        upButton.addEventListener('click', () => this.step(true));

        const downButton = document.createElement('button');
        downButton.textContent = '▼';
        downButton.className = 'number-input-button down';
        downButton.addEventListener('click', () => this.step(false));

        buttonContainer.appendChild(upButton);
        buttonContainer.appendChild(downButton);

        container.appendChild(input);
        container.appendChild(buttonContainer);

        return container;
    }

    /**
     * Handle input event
     * @param {Event} event - Input event
     */
    handleInput(event) {
        const input = event.target;
        const value = parseFloat(input.value);
        
        if (isNaN(value)) {
            this.setCustomValidity(input, 'Invalid number');
            return;
        }
        
        if (this.validateValue(value)) {
            this.value = value;
            this.lastValidValue = value;
            this.setCustomValidity(input, '');
        } else {
            this.setCustomValidity(input, this.getValidationMessage(value));
        }
    }

    /**
     * Handle blur event
     * @param {Event} event - Blur event
     */
    handleBlur(event) {
        const input = event.target;
        
        // If the current value is invalid, revert to the last valid value
        if (!input.checkValidity()) {
            input.value = this.lastValidValue;
            this.setCustomValidity(input, '');
        }
    }

    /**
     * Handle keydown event
     * @param {Event} event - Keydown event
     */
    handleKeyDown(event) {
        // Handle up/down arrow keys
        if (event.key === 'ArrowUp') {
            event.preventDefault();
            this.step(true);
        } else if (event.key === 'ArrowDown') {
            event.preventDefault();
            this.step(false);
        }
    }

    /**
     * Step the value up or down
     * @param {boolean} up - Whether to step up or down
     */
    step(up) {
        const input = this.querySelector('input');
        const currentValue = parseFloat(input.value) || 0;
        const step = this.schema.multipleOf || 0.1;
        
        let newValue = up ? currentValue + step : currentValue - step;
        
        // Round to avoid floating point precision issues
        const precision = this.getPrecision(step);
        newValue = parseFloat(newValue.toFixed(precision));

        if (this.validateValue(newValue)) {
            this.value = newValue;
            this.lastValidValue = newValue;
            input.value = newValue;
            this.setCustomValidity(input, '');
        }
    }

    /**
     * Validate a value against the schema
     * @param {number} value - Value to validate
     * @returns {boolean} - Whether the value is valid
     */
    validateValue(value) {
        if (typeof value !== 'number' || !isFinite(value)) {
            return false;
        }

        if (this.schema.minimum !== undefined && value < this.schema.minimum) {
            return false;
        }

        if (this.schema.maximum !== undefined && value > this.schema.maximum) {
            return false;
        }

        if (this.schema.multipleOf !== undefined && value % this.schema.multipleOf !== 0) {
            return false;
        }

        return true;
    }

    /**
     * Get a validation message for a value
     * @param {number} value - Value to validate
     * @returns {string} - Validation message
     */
    getValidationMessage(value) {
        if (typeof value !== 'number' || !isFinite(value)) {
            return 'Please enter a valid number';
        }

        if (this.schema.minimum !== undefined && value < this.schema.minimum) {
            return `Value must be greater than or equal to ${this.schema.minimum}`;
        }

        if (this.schema.maximum !== undefined && value > this.schema.maximum) {
            return `Value must be less than or equal to ${this.schema.maximum}`;
        }

        if (this.schema.multipleOf !== undefined && value % this.schema.multipleOf !== 0) {
            return `Value must be a multiple of ${this.schema.multipleOf}`;
        }

        return '';
    }

    /**
     * Set custom validity on an input
     * @param {HTMLInputElement} input - Input element
     * @param {string} message - Validation message
     */
    setCustomValidity(input, message) {
        input.setCustomValidity(message);
        
        // Update visual feedback
        if (message) {
            input.classList.add('invalid');
            input.title = message;
        } else {
            input.classList.remove('invalid');
            input.title = this.schema.description || '';
        }
    }

    /**
     * Get the precision of a number
     * @param {number} number - Number to get precision of
     * @returns {number} - Precision
     */
    getPrecision(number) {
        const str = number.toString();
        const decimalIndex = str.indexOf('.');
        return decimalIndex === -1 ? 0 : str.length - decimalIndex - 1;
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
        if (this.validateValue(value)) {
            this.value = value;
            this.lastValidValue = value;
            const input = this.querySelector('input');
            if (input) {
                input.value = value;
                this.setCustomValidity(input, '');
            }
        }
    }

    /**
     * Query selector for the container
     * @param {string} selector - Selector
     * @returns {HTMLElement} - Element
     */
    querySelector(selector) {
        return this.container ? this.container.querySelector(selector) : null;
    }
}
