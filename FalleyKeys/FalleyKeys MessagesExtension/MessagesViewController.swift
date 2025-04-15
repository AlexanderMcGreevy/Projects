import UIKit
import Messages
import CoreMotion

class MessagesViewController: MSMessagesAppViewController {
    
    let motionManager = CMMotionManager()
    var animator: UIDynamicAnimator!
    var gravity: UIGravityBehavior!
    var collision: UICollisionBehavior!
    var dynamicItemBehavior: UIDynamicItemBehavior!
    var keyButtons: [UIButton] = []
    let keyboardLetters = Array("QWERTYUIOPASDFGHJKLZXCVBNM")
    let typedLabel = UILabel()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupPhysics()
        setupKeyboard()
        setupTypedLabel()
        startMotionUpdates()
    }
    
    func setupPhysics() {
        animator = UIDynamicAnimator(referenceView: self.view)
        
        gravity = UIGravityBehavior()
        animator.addBehavior(gravity)
        
        collision = UICollisionBehavior()
        collision.translatesReferenceBoundsIntoBoundary = true
        animator.addBehavior(collision)
        
        dynamicItemBehavior = UIDynamicItemBehavior()
        dynamicItemBehavior.elasticity = 0.6
        dynamicItemBehavior.friction = 0.2
        dynamicItemBehavior.allowsRotation = true
        animator.addBehavior(dynamicItemBehavior)
    }

    func setupTypedLabel() {
        typedLabel.frame = CGRect(x: 10, y: 20, width: view.bounds.width - 20, height: 40)
        typedLabel.font = UIFont.systemFont(ofSize: 24, weight: .bold)
        typedLabel.textColor = .label
        typedLabel.textAlignment = .center
        typedLabel.text = ""
        view.addSubview(typedLabel)
    }

    func setupKeyboard() {
        for letter in keyboardLetters {
            let size: CGFloat = 45
            let x = CGFloat.random(in: 20...(view.bounds.width - size - 20))
            let y = CGFloat.random(in: 80...(view.bounds.height - size - 20))
            let button = UIButton(frame: CGRect(x: x, y: y, width: size, height: size))
            button.setTitle(String(letter), for: .normal)
            button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 22)
            button.backgroundColor = .systemBlue
            button.setTitleColor(.white, for: .normal)
            button.layer.cornerRadius = 8
            button.addTarget(self, action: #selector(keyPressed(_:)), for: .touchUpInside)
            
            view.addSubview(button)
            keyButtons.append(button)
            
            gravity.addItem(button)
            collision.addItem(button)
            dynamicItemBehavior.addItem(button)
        }
    }

    @objc func keyPressed(_ sender: UIButton) {
        guard let letter = sender.title(for: .normal) else { return }
        typedLabel.text?.append(letter)
    }
    
    func startMotionUpdates() {
        guard motionManager.isAccelerometerAvailable else { return }
        motionManager.accelerometerUpdateInterval = 0.1
        motionManager.startAccelerometerUpdates(to: .main) { [weak self] data, _ in
            guard let self = self, let acceleration = data?.acceleration else { return }
            // Map device motion to gravity direction
            let x = CGFloat(acceleration.x)
            let y = CGFloat(-acceleration.y)
            self.gravity.gravityDirection = CGVector(dx: x, dy: y)
        }
    }
}
